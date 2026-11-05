from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.tools import tool

load_dotenv()

@tool
def add_numbers(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b

llm = ChatGroq(model="openai/gpt-oss-20b", temperature=0)

tools = [add_numbers]
llm_with_tools = llm.bind_tools(tools)

response = llm_with_tools.invoke("Calculate 125 + 275.")

# Execute requested tools
tool_map = {tool.name: tool for tool in tools}
tool_call = response.tool_calls[0]
result = tool_map[tool_call["name"]].invoke(tool_call["args"])
print("Tool result:", result)

