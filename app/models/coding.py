from pydantic import BaseModel

class CodingResult(BaseModel):
    filename:str
    content:str
    