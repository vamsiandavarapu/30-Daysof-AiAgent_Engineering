from langchain_core.tools import tool

# Define a tool
@tool
def add_numbers(a: int, b: int) -> int:
    """Add two numbers and return their sum."""
    return a + b


# Inspect the tool
print("Tool name:", add_numbers.name)
print("Tool description:", add_numbers.description)
print("Tool input schema:", add_numbers.args)


# Execute the tool directly
result = add_numbers.invoke({
    "a": 15,
    "b": 25
})

print("Tool result:", result)
