from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain_groq import ChatGroq

load_dotenv()
# 1. Define the output schema
class ConceptInfo(BaseModel):
    concept: str = Field(description="Name of the concept")
    category: str = Field(description="Concept category")
    difficulty: str = Field(description="Difficulty level")
    applications: list[str] = Field(
        description="Practical applications" )

# 2. Initialize the model
llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0
)

# 3. Attach the schema to the model
structured_llm = llm.with_structured_output(ConceptInfo)

# 4. Invoke the model
response = structured_llm.invoke(
    "Explain Random Forest in machine learning."
)

# 5. Access the structured response
print(response)

print("\nConcept:", response.concept)
print("Category:", response.category)
print("Difficulty:", response.difficulty)
print("Applications:", response.applications)

# Convert the Pydantic object into a dictionary
print("\nDictionary:", response.model_dump())
