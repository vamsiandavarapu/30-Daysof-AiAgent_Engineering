from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.tools import tool

load_dotenv()

# Define the tool
@tool
def add_numbers(a: int, b: int) -> int:
    """Add two numbers and return their sum."""
    return a + b

@tool
def subtract_numbers(a: int, b: int) -> int:
    """Subtract two numbers and return their difference."""
    return a - b

llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0
)

# Bind the tools to the model
llm_with_tools = llm.bind_tools([add_numbers, subtract_numbers])

# Send a request to the model
response = llm_with_tools.invoke(
    "Use the subtract_numbers tool to calculate 225 - 275."
)

print("AI response:", response.content)
print("\nTool calls:", response.tool_calls)
