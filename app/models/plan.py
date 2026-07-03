from enum import Enum
from pydantic import BaseModel

class AgentType(Enum):
    PLANNER = "planner"
    RESEARCH = "research"
    CODING = "coding"
    REVIEW = "review"
    WRITER = "writer"
    
class PlanStep(BaseModel):
    agent:AgentType
    task:str

class Plan(BaseModel):
    needs_research: bool
    response: list[PlanStep]
    reason:str


