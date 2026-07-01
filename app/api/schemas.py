from pydantic import BaseModel

class Message(BaseModel):
    role: str
    content: str

class GenerateRequest(BaseModel):
    messages : list[Message]
    model : str | None = None
    temperature : float = 0.2