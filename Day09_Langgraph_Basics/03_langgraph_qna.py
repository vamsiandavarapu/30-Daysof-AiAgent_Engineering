import os
from typing import TypedDict
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, START, END

load_dotenv()

# Initialize LLM
model = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0.2
)

# Define state
class QAState(TypedDict):
    question: str
    answer: str

# LLM node
def generate_answer(state: QAState):
    response = model.invoke(state["question"])
    return {"answer": response.content}

# Build graph
graph = StateGraph(QAState)

graph.add_node("answer", generate_answer)

graph.add_edge(START, "answer")
graph.add_edge("answer", END)

app = graph.compile()

# User interaction
while True:
    question = input("\nYou: ")

    if question.lower() in ["exit", "quit"]:
        break

    result = app.invoke({
        "question": question,
        "answer": ""
    })

    print("\nAssistant:", result["answer"])
