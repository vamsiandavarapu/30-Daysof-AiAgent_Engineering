from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage

load_dotenv()

llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0
)

# Define the conversation messages
messages = [
    SystemMessage(
        content="You are a helpful Data Science tutor. Explain concepts clearly."
    ),
    HumanMessage(
        content="What is overfitting in machine learning?"
    )
]

response = llm.invoke(messages)

print("AI:", response.content)

# Continue the conversation using the previous messages
messages.append(response)
messages.append(
    HumanMessage(
        content="How can we prevent it?"
    )
)
# Invoke the model with the conversation history
follow_up_response = llm.invoke(messages)

print("\nAI:", follow_up_response.content)
