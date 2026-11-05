from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.tools import tool

load_dotenv()

@tool
def add_numbers(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b

@tool
def multiply_numbers(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b

@tool
def word_count(text: str) -> int:
    """Count the number of words in a text."""
    return len(text.split())

llm = ChatGroq(model="openai/gpt-oss-20b", temperature=0)

# Make all tools available to the model
tools = [add_numbers, multiply_numbers, word_count]
llm_with_tools = llm.bind_tools(tools)

# Ask the model to select a tool
response = llm_with_tools.invoke(
    "How many words are in this sentence: 'LangChain makes it easy to build applications with language models'?"
)

print("Tool calls:", response.tool_calls)

# Execute the requested tools
tool_map = {t.name: t for t in tools}

for call in response.tool_calls:
    result = tool_map[call["name"]].invoke(call["args"])
    print("Selected tool:", call["name"])
    print("Result:", result)
