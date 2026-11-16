from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

class TicketState(TypedDict):
    ticket:str
    category:str
    result:str
    
llm=ChatGroq(model="openai/gpt-oss-20b",temperature=0)
def check_ticket(state):
    return { "ticket": state["ticket"].lower()}

def billing(state):
    return {"result":"Billing team will contact you"}

def technical(state):
    return {"result":"Technical team will investigate"}

def account(state):
    return {"result":"Accounts team will check and contact"}

    
def router(state):
    prompt=f"""Categorize this ticket as:
        billing, technical, or account
    
        Ticket:
        {state["ticket"]}
        just return the exact category name not more than that.
        """
    response=llm.invoke(prompt)
    state["category"]=response.content.strip().lower()
    
    print(response.content.strip().lower())
    return state["category"]
    

graph=StateGraph(TicketState)

graph.add_node("check",check_ticket)
graph.add_node("billing",billing)
graph.add_node("technical",technical)
graph.add_node("account",account)

graph.add_edge(START,"check")
graph.add_conditional_edges(
    "check",
    router
)
graph.add_edge("billing",END)
graph.add_edge("technical",END)
graph.add_edge("account",END)

app=graph.compile()
res=app.invoke({
    "ticket":input("Enter you ticket:")
})

print(res)
