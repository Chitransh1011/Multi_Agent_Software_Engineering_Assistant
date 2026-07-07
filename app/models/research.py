from pydantic import BaseModel,Field

class ResearchResult(BaseModel):
    summary:str
    references:list[str] = Field(default_factory=list)

