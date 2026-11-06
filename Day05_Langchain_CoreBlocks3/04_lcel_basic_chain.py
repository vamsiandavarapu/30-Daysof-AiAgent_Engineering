from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

# 1. Initialize the model
llm = ChatGroq(model="openai/gpt-oss-20b", temperature=0)

# 2. Create a prompt template
prompt = ChatPromptTemplate.from_template(
    "Explain {topic} in simple terms with one example."
)

# 3. Create an output parser
parser = StrOutputParser()

# 4. Connect components using LCEL
chain = prompt | llm | parser

# 5. Execute the chain
response = chain.invoke({"topic": "Random Forest"})

print(response)
