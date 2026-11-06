from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser

load_dotenv()

llm=ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0
)

#1. String Output Parser
response=llm.invoke("Explain Machine Learning in two sentences.")

str_parser=StrOutputParser()
text_result=str_parser.invoke(response)

print("String Output:")
print(text_result)
print("Type:", type(text_result))


#2. JsonOutput Parser
json_parser=JsonOutputParser()

prompt=f"""
Identify the skills required for a Python Developer.
{json_parser.get_format_instructions()}

Return the following fields:
job_title, required_skills, experience_level.
"""

response=llm.invoke(prompt)

json_result=json_parser.invoke(response)

print("\nJSON Output:")
print(json_result)

print("\nJob Title:", json_result["job_title"])
print("Skills:", json_result["required_skills"])