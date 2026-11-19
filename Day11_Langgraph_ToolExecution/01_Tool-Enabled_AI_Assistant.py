import os
from datetime import datetime

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.tools import tool
from langchain_core.messages import SystemMessage

from langgraph.graph import StateGraph, START, MessagesState
from langgraph.prebuilt import ToolNode, tools_condition

# 1. Load environment variables

load_dotenv()

if not os.getenv("GROQ_API_KEY"):
    raise ValueError("GROQ_API_KEY is missing from .env")

# 2. Define Python tools
@tool
def calculator(a: float, b: float, operation: str) -> str:
    """Perform addition, subtraction, multiplication or division."""

    if operation == "add":
        result = a + b
    elif operation == "subtract":
        result = a - b
    elif operation == "multiply":
        result = a * b
    elif operation == "divide":
        if b == 0:
            raise ValueError("Cannot divide by zero")
        result = a / b
    else:
        raise ValueError("Invalid operation")
    return str(result)

@tool
def text_analyzer(text: str) -> str:
    """Count the words and characters in a given text."""
    words = len(text.split())
    characters = len(text)
    return f"Words: {words}, " f"Characters including spaces: {characters}"


@tool
def get_datetime() -> str:
    """Get the current local date, time and timezone."""
    return datetime.now().astimezone().strftime("%d-%m-%Y %I:%M:%S %p %Z")

# 3. Register tools
tools = [calculator, text_analyzer, get_datetime]

# 4. Initialize Groq LLM
llm = ChatGroq(model="openai/gpt-oss-20b", temperature=0)

# Make tools available to the LLM
llm_with_tools = llm.bind_tools(tools)

# 5. Define chatbot node
def chatbot(state: MessagesState):
    system_message = SystemMessage(content="""
        You are a helpful Personal AI Utility Assistant.

        You can perform three tasks:

        1. Calculator:
           Perform arithmetic calculations.

        2. Text Analyzer:
           Count words and characters.

        3. Date and Time:
           Get the current local date and time.

        Instructions:
        - Use the appropriate tool when required.
        - Never invent tool results.
        - Explain results clearly.
        - If a user asks for multiple independent tasks,
          you may call multiple tools.
        - For general questions, respond normally.
        """)

    response = llm_with_tools.invoke([system_message] + state["messages"])
    return {"messages": [response]}

# 6. Create LangGraph
builder = StateGraph(MessagesState)

# Add chatbot node
builder.add_node("chatbot", chatbot)

# Add ToolNode
builder.add_node("tools", ToolNode(tools, handle_tool_errors=True))

# 7. Define graph edges
builder.add_edge(START, "chatbot")

# Route based on whether the LLM requested tools
builder.add_conditional_edges("chatbot", tools_condition)

# Return tool results to the chatbot
builder.add_edge("tools", "chatbot")

# 8. Compile graph
app = builder.compile()

# 9. Run assistant
print("\nPersonal AI Utility Assistant")
print("Available tools: Calculator, Text Analyzer, Date & Time")
print("Type 'exit' to stop.\n")

while True:
    user_input = input("You: ").strip()

    if user_input.lower() in ["exit", "quit"]:
        print("Assistant: Goodbye!")
        break

    if not user_input:
        continue

    try:
        result = app.invoke({"messages": [{"role": "user", "content": user_input}]})
        print("\nAssistant:")
        print(result["messages"][-1].content)
        print()

    except Exception as e:
        print("\nError:", e)
