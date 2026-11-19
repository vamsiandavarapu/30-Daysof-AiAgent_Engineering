import os
import sqlite3

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage

from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.checkpoint.sqlite import SqliteSaver

# 1. Load environment variables
load_dotenv()

if not os.getenv("GROQ_API_KEY"):
    raise ValueError("GROQ_API_KEY is missing from .env")

# 2. Initialize Groq LLM
llm = ChatGroq(model="openai/gpt-oss-20b", temperature=0)

# 3. Define chatbot node
def chatbot(state: MessagesState):
    system_message = SystemMessage(content="""
        You are a helpful conversational AI assistant.

        Remember the information available in the
        conversation history.

        Answer questions using previous messages
        whenever relevant.

        If you don't know something, say so.
        Do not invent personal information.
        """)

    response = llm.invoke([system_message] + state["messages"])
    return {"messages": [response]}

# 4. Create LangGraph
builder = StateGraph(MessagesState)
builder.add_node("chatbot", chatbot)
builder.add_edge(START, "chatbot")
builder.add_edge("chatbot", END)

# 5. Create SQLite connection
conn = sqlite3.connect("assistant_memory.db", check_same_thread=False)
checkpointer = SqliteSaver(conn)
# Create checkpoint tables if needed
checkpointer.setup()

# 6. Compile graph with checkpointer
app = builder.compile(checkpointer=checkpointer)

# 7. Configure conversation thread
thread_id = input("Enter your conversation ID: ").strip()

if not thread_id:
    thread_id = "user_101"

config = {"configurable": {"thread_id": thread_id}}

# 8. Run conversational assistant
print("\nStateful AI Assistant Started!")
print("Type 'history' to inspect saved messages.")
print("Type 'exit' to stop.\n")

try:
    while True:
        user_input = input("You: ").strip()

        if user_input.lower() in ["exit", "quit"]:
            print("Assistant: Goodbye!")
            break

        if not user_input:
            continue

        # Retrieve saved conversation state
        if user_input.lower() == "history":
            snapshot = app.get_state(config)

            messages = snapshot.values.get("messages", [])

            print("\nConversation History:")

            for message in messages:
                print(f"{message.type}: {message.content}")

            print()
            continue

        try:
            result = app.invoke(
                {"messages": [{"role": "user", "content": user_input}]}, config=config
            )

            print("\nAssistant:", result["messages"][-1].content, "\n")

        except Exception as e:
            print("\nError:", e)

finally:
    conn.close()
