
from typing import TypedDict
from langgraph.graph import StateGraph, START, END

class NumberState(TypedDict):
    number: int
    result: str

# Node 1: Check number
def check_number(state: NumberState):
    return {"number": state["number"]}

# Node 2: Even processing
def even_node(state: NumberState):
    return {"result": "The number is Even"}

# Node 3: Odd processing
def odd_node(state: NumberState):
    return {"result": "The number is Odd"}

# Routing function
def decide(state: NumberState):
    if state["number"] % 2 == 0:
        return "even"
    return "odd"

# Build graph
graph = StateGraph(NumberState)

graph.add_node("check", check_number)
graph.add_node("even", even_node)
graph.add_node("odd", odd_node)

graph.add_edge(START, "check")

graph.add_conditional_edges(
    "check",
    decide,
    {
        "even": "even",
        "odd": "odd"
    }
)

graph.add_edge("even", END)
graph.add_edge("odd", END)

app = graph.compile()

result = app.invoke({
    "number": 7,
    "result": ""
})

print(result["result"])
