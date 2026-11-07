from pydantic import BaseModel, Field

class ResearchSource(BaseModel):
    title: str = Field(description="Title of the source")
    url: str = Field(
        description="URL of the source"
    )
    snippet: str = Field(
        description="Short description or relevant information from the source"
    )


class ResearchReport(BaseModel):
    research_question: str = Field(
        description="The original research question asked by the user"
    )
    summary: str = Field(
        description="A concise summary of the research findings"
    )
    key_findings: list[str] = Field(
        description="A list of important findings discovered during research"
    )
    sources: list[ResearchSource] = Field(
        description="Sources used to support the research findings"
    )
