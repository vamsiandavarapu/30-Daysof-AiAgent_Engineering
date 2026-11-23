import sqlite3

from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.types import interrupt, Command


# 1. Define graph state
class ApprovalState(TypedDict):
    action: str
    approved: bool


# 2. Prepare action
def prepare_action(state: ApprovalState):
    print("\nPreparing action:", state["action"])
    return {}


# 3. Pause and request human approval
def approval_node(state: ApprovalState):
    print("Hello")
    decision = interrupt(
        {"message": "Do you approve this action?", "action": state["action"]}
    )
    return {"approved": decision}


# 4. Decide the next node
def approval_router(state: ApprovalState):
    if state["approved"]:
        return "execute"
    return "reject"


# 5. Execute approved action
def execute_action(state: ApprovalState):
    print("\n[EXECUTED]", state["action"])
    return {}


# 6. Handle rejection
def reject_action(state: ApprovalState):
    print("\n[REJECTED] Action was not executed.")
    return {}


# 7. Build graph
builder = StateGraph(ApprovalState)

builder.add_node("prepare", prepare_action)
builder.add_node("approval", approval_node)
builder.add_node("execute", execute_action)
builder.add_node("reject", reject_action)

builder.add_edge(START, "prepare")
builder.add_edge("prepare", "approval")
builder.add_conditional_edges(
    "approval", approval_router, {"execute": "execute", "reject": "reject"}
)
builder.add_edge("execute", END)
builder.add_edge("reject", END)

# 8. Configure SQLite checkpointer
conn = sqlite3.connect("approval.db", check_same_thread=False)
checkpointer = SqliteSaver(conn)
checkpointer.setup()

app = builder.compile(checkpointer=checkpointer)

# 9. Start workflow
try:
    action = input("Enter an action: ").strip()

    if not action:
        raise ValueError("Action cannot be empty.")
    thread_id = input("Enter thread ID: ").strip()

    if not thread_id:
        raise ValueError("Thread ID is required.")

    config = {"configurable": {"thread_id": thread_id}}
    result = app.invoke({"action": action, "approved": False}, config=config)

    # 10. Check whether the graph paused
    if result.get("__interrupt__"):
        for item in result["__interrupt__"]:
            print("\nApproval request:", item.value)
        choice = input("\nApprove this action? (yes/no): ").strip().lower()
        if choice not in ["yes", "no"]:
            print("Invalid decision. Workflow remains paused.")
        else:
            result = app.invoke(Command(resume=(choice == "yes")), config=config)
    print("\nWorkflow state:")
    print(app.get_state(config).values)

finally:
    conn.close()

from IPython.display import Image, display
display(Image(app.get_graph().draw_mermaid_png()))
print(app.get_graph().draw_mermaid())
