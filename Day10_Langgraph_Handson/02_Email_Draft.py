from typing import TypedDict
from dotenv import load_dotenv
from langgraph.graph import StateGraph, START, END
from langchain_groq import ChatGroq

load_dotenv()

llm = ChatGroq(model="openai/gpt-oss-20b")


class EmailState(TypedDict):
    prompt: str
    draft: str
    approved: bool
    feedback: str


def draft_email(state):
    response = llm.invoke(f"Write a professional email for:\n{state['prompt']}")

    return {"draft": response.content}


def review_email(state):
    print("\n" + "=" * 60)
    print("EMAIL DRAFT")
    print("=" * 60)
    print(state["draft"])
    print("=" * 60)

    choice = input("\nApprove email? (yes/no): ").strip().lower()

    if choice == "yes":
        return {"approved": True, "feedback": ""}

    feedback = input("Enter your feedback for rewriting: ")

    return {"approved": False, "feedback": feedback}


def rewrite_email(state):
    response = llm.invoke(f"""
        Rewrite the email based on the user's feedback.

        Original Email:
        {state['draft']}

        User Feedback:
        {state['feedback']}

        Generate the improved email.
        """)

    return {"draft": response.content}


def router(state):
    if state["approved"]:
        return "end"

    return "rewrite"


graph = StateGraph(EmailState)

graph.add_node("draft", draft_email)
graph.add_node("review", review_email)
graph.add_node("rewrite", rewrite_email)

graph.add_edge(START, "draft")
graph.add_edge("draft", "review")

graph.add_conditional_edges("review", router, {"rewrite": "rewrite", "end": END})

graph.add_edge("rewrite", "review")

app = graph.compile()


if __name__ == "__main__":

    user_prompt = input("What email would you like to write?\n> ")

    result = app.invoke(
        {"prompt": user_prompt, "draft": "", "approved": False, "feedback": ""}
    )

    print("\nFINAL APPROVED EMAIL:\n")
    print(result["draft"])
