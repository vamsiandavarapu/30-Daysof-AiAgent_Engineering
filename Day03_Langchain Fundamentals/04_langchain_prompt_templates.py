from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0
)

# Create a reusable chat prompt template
prompt_template = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are an expert {subject} tutor. "
        "Explain concepts in a simple and practical way."
    ),
    (
        "human",
        "Explain {topic} with a practical example."
    )
])

# Provide dynamic values to the template
formatted_messages = prompt_template.invoke({
    "subject": "Data Science",
    "topic": "Random Forest"
})

response = llm.invoke(formatted_messages)

print(response.content)
