from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

# Initialize the model
llm = ChatGroq(model="openai/gpt-oss-20b", temperature=0)

# Create prompt
prompt = ChatPromptTemplate.from_template("Explain {topic} with a practical example.")

# Create parser
parser = StrOutputParser()

# Build LCEL chain
chain = prompt | llm | parser

# Stream the response
for chunk in chain.stream({"topic": "Retrieval-Augmented Generation"}):
    print(chunk, end="", flush=True)
