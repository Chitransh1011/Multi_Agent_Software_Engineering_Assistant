from pydantic import BaseModel

class CodingResult(BaseModel):
    filename:str
    artifact_type:str
    content:str
    