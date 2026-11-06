from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0
)

# 1. Single request
response = llm.invoke("What is Machine Learning?")
print("Invoke:", response.content)

# 2. Multiple independent requests
questions = [
    "What is supervised learning?",
    "What is unsupervised learning?",
    "What is overfitting?"
]

responses = llm.batch(questions)

for response in responses:
    print("\n", response.content)


for chunk in llm.stream("Explain neural networks."):
    print(chunk.content, end="", flush=True)