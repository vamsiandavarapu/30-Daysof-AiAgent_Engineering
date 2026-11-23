import math
import os
from typing import Any, Literal, TypedDict

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, START, END
from pydantic import BaseModel, Field

# 1. Define graph state
class GuardrailState(TypedDict):
    tool_name: str
    arguments: dict
    allowed: bool
    result: Any
    error: str


class ToolSelection(BaseModel):
    tool_name: Literal["calculator", "text_analyzer", "unsupported"] = Field(
        description="The one tool that best matches the user's request, or unsupported."
    )
    arguments: dict[str, Any] = Field(
        description="Arguments for the selected tool, using only its required keys."
    )


# 2. Calculator tool
def calculator(operation, a, b):
    operations = {
        "add": lambda: a + b,
        "subtract": lambda: a - b,
        "multiply": lambda: a * b,
        "divide": lambda: a / b,
    }
    if operation not in operations:
        raise ValueError("Unsupported calculator operation")
    if operation == "divide" and b == 0:
        raise ValueError("Division by zero is not allowed")
    return operations[operation]()


# 3. Text analyzer tool
def text_analyzer(text):
    return {"characters": len(text), "words": len(text.split())}

# 4. Approved tool registry
TOOLS = {"calculator": calculator, "text_analyzer": text_analyzer}

# 5. Validate requested tool and arguments
def validate_request(state: GuardrailState):
    tool_name = state["tool_name"]
    args = state["arguments"]
    try:
        if tool_name not in TOOLS:
            raise ValueError("Tool is not permitted")
        if not isinstance(args, dict):
            raise ValueError("Arguments must be a dictionary")
        if tool_name == "calculator":
            if set(args) != {"operation", "a", "b"}:
                raise ValueError("Invalid calculator arguments")
            if args["operation"] not in ["add", "subtract", "multiply", "divide"]:
                raise ValueError("Operation is not permitted")
            for key in ["a", "b"]:
                value = args[key]
                if isinstance(value, bool) or not isinstance(value, (int, float)):
                    raise ValueError(f"{key} must be numeric")

                if isinstance(value, float) and not math.isfinite(value):
                    raise ValueError(f"{key} must be finite")

                if abs(value) > 1_000_000_000:
                    raise ValueError(f"{key} exceeds the allowed limit")

            if args["operation"] == "divide" and args["b"] == 0:
                raise ValueError("Division by zero is not allowed")
        elif tool_name == "text_analyzer":
            if set(args) != {"text"}:
                raise ValueError("Invalid text analyzer arguments")

            if not isinstance(args["text"], str):
                raise ValueError("Text must be a string")

            if len(args["text"]) > 5000:
                raise ValueError("Text exceeds the 5000-character limit")

        return {"allowed": True, "error": ""}

    except (ValueError, TypeError) as e:
        return {"allowed": False, "error": str(e)}


# 6. Route valid and invalid requests
def validation_router(state: GuardrailState):
    if state["allowed"]:
        return "execute"
    return "block"


# 7. Execute permitted tool
def execute_tool(state: GuardrailState):
    try:
        result = TOOLS[state["tool_name"]](**state["arguments"])
        return {"result": result, "error": ""}
    except Exception as e:
        return {"result": None, "error": f"Tool execution failed: {e}"}


# 8. Validate tool output
def validate_output(state: GuardrailState):
    result = state["result"]
    if result is None:
        return {"error": "Tool returned an empty result"}
    if isinstance(result, float) and not math.isfinite(result):
        return {"error": "Tool returned a non-finite number"}
    if isinstance(result, dict):
        if not all(isinstance(value, int) and value >= 0 for value in result.values()):
            return {"error": "Tool returned an invalid result"}
    return {}

# 9. Route execution result
def result_router(state: GuardrailState):
    if state["error"]:
        return "block"
    return "success"

# 10. Handle blocked requests
def block_request(state: GuardrailState):
    print("\n[BLOCKED]", state["error"])
    return {}

# 11. Display successful result
def show_result(state: GuardrailState):
    print("\n[SUCCESS]", state["result"])
    return {}

# 12. Build LangGraph workflow
builder = StateGraph(GuardrailState)

builder.add_node("validate", validate_request)
builder.add_node("execute", execute_tool)
builder.add_node("check_output", validate_output)
builder.add_node("block", block_request)
builder.add_node("success", show_result)

builder.add_edge(START, "validate")
builder.add_conditional_edges(
    "validate", validation_router, {"execute": "execute", "block": "block"}
)
builder.add_conditional_edges("execute", result_router, {"success": "check_output", "block": "block"})
builder.add_conditional_edges(
    "check_output", result_router, {"success": "success", "block": "block"}
)

builder.add_edge("success", END)
builder.add_edge("block", END)

app = builder.compile()

# 13. Let the LLM select a tool and its arguments
if __name__ == "__main__":
    load_dotenv()
    if not os.getenv("GROQ_API_KEY"):
        raise RuntimeError("GROQ_API_KEY is missing. Add it to your .env file.")

    llm = ChatGroq(model="openai/gpt-oss-20b", temperature=0)
    tool_selector = llm.with_structured_output(
        ToolSelection, method="function_calling"
    )

    user_request = input("\nWhat would you like me to do? ").strip()
    if not user_request:
        raise ValueError("Request cannot be empty.")

    selection = tool_selector.invoke([
        (
            "system",
            "Choose exactly one tool based on the user's request. "
            "For calculator, return arguments with exactly operation, a, and b. "
            "For text_analyzer, return arguments with exactly text. "
            "If neither tool can handle the request, choose unsupported and return "
            "an empty arguments object. Do not perform the calculation or analysis.",
        ),
        ("human", user_request),
    ])
    tool_name = selection.tool_name
    arguments = selection.arguments
    print(f"\nLLM selected tool: {tool_name}")

    initial_state = {
        "tool_name": tool_name,
        "arguments": arguments,
        "allowed": False,
        "result": None,
        "error": "",
    }

    app.invoke(initial_state)
    
    
