from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.tools import tool
from langchain.agents import create_agent

load_dotenv()

@tool
def add_numbers(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b


@tool
def multiply_numbers(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b


# Initialize the model
llm = ChatGroq(model="openai/gpt-oss-20b", temperature=0)

# Create the agent
agent = create_agent(
    model=llm,
    tools=[add_numbers, multiply_numbers],
    system_prompt="You are a helpful mathematical assistant.",
)

# Invoke the agent
result = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": "Add 250 and 350. Multiply 25 by 12, then add 100.Add 50, multiply the result by 3, and explain the calculation. and tell me did you used any tools",
            }
        ]
    }
)

print("Final Answer:", result["messages"][-1].content)
