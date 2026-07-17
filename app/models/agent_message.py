from pydantic import BaseModel

class AgentMessage(BaseModel):
    agent_name: str
    role: str
    content: str