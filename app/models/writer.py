from pydantic import BaseModel

class WriterResult(BaseModel):
    title: str
    summary: str
    review_summary: str