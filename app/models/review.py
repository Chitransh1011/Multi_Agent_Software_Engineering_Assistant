from pydantic import BaseModel,Field
from app.graph.state import AgentType
class ReviewResult(BaseModel):
    passed:bool
    confidence: float
    feedback: str
    issues: list[str]=Field(default_factory=list)
    next_action: AgentType
    retry_task: str | None = None