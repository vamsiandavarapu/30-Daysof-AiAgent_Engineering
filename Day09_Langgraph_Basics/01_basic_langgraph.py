from typing import TypedDict
from langgraph.graph import StateGraph, START, END

#Define state
class CalculatorState(TypedDict):
    a:int
    b:int
    result:int
    
#Node1 Creation
def add(state:CalculatorState):
    result=state["a"]+state["b"]
    return {"result":result}

#Node2 Creation
def Multiplication(state:CalculatorState):
    result=state["result"]*2
    return {"result":result}
    
#Create Graph
graph = StateGraph(CalculatorState)

graph.add_node("add",add)
graph.add_node("multiply",Multiplication)

graph.add_edge(START,"add")
graph.add_edge("add","multiply")
graph.add_edge("multiply",END)

#Compile and execute
app=graph.compile()

result=app.invoke({
    "a":10,
    "b":5,
    "result":0
})

print("Final Result:", result["result"])
