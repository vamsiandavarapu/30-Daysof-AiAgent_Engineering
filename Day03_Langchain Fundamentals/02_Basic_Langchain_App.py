from dotenv import load_dotenv
from langchain_groq import ChatGroq

# Load environment variables from .env
load_dotenv()

# Initialize the chat model
model = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0
)

# Send a request to the model
response = model.invoke(
    "Explain the difference between AI and Machine Learning."
)

# Display the response
print(response.content)
