from pydantic import BaseModel

class Message(BaseModel):
    role: str
    content: str

class GenerateRequest(BaseModel):
    user_query:str