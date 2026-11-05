from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, ToolMessage

load_dotenv()

@tool
def add_numbers(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b


@tool
def subtract_numbers(a: int, b: int) -> int:
    """Subtract the second number from the first."""
    return a - b


@tool
def multiply_numbers(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b


@tool
def divide_numbers(a: int, b: int) -> float:
    """Divide the first number by the second."""
    return a / b


llm = ChatGroq(model="openai/gpt-oss-20b", temperature=0)

tools = [add_numbers, subtract_numbers, multiply_numbers, divide_numbers]
tool_map = {t.name: t for t in tools}

llm_with_tools = llm.bind_tools(tools)

# 1. Send user request
messages = [
    HumanMessage(
        content="What is 275 minus 125, 12 multiplied by 5, and 275 divided by 5?"
    )
]

response = llm_with_tools.invoke(messages)
messages.append(response)

# 2. Execute requested tools
for call in response.tool_calls:
    result = tool_map[call["name"]].invoke(call["args"])

    # 3. Send tool result back to the LLM
    messages.append(
        ToolMessage(
            content=str(result),
            tool_call_id=call["id"]
        )
    )

# 4. Get final response
final_response = llm_with_tools.invoke(messages)

print(final_response.content)
