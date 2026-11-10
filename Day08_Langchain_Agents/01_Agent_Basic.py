from langchain.agents import create_agent
from langchain_groq import ChatGroq
from langchain.tools import tool
from dotenv import load_dotenv

load_dotenv()

# Define tools


@tool
def add_numbers(a: int, b: int) -> int:
    """Add two numbers"""
    print("Tool used:add")
    return a + b


@tool
def multiply_numbers(a: int, b: int) -> int:
    """Multiply two numbers"""
    print("Tool used:multiplication")
    return a * b


# Initialize model
model = ChatGroq(model="openai/gpt-oss-20b", temperature=0)

# Create agent
agent = create_agent(
    model=model,
    tools=[add_numbers, multiply_numbers],
    system_prompt="You are a helpful mathematical assistant",
)

# Execute agent
result = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": "Add 120 and 80, then multiply the result by 3.",
            }
        ]
    }
)

print(result["messages"][-1].content)

# Inspect the complete message sequence
for message in result["messages"]:

    print("\nMessage type:", message.type)

    if message.type == "ai":
        print("Content:", message.content)
        print("Tool calls:", message.tool_calls)

    elif message.type == "tool":
        print("Tool name:", message.name)
        print("Tool result:", message.content)

    else:
        print("Content:", message.content)
