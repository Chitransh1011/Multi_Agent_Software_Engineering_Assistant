from pydantic import BaseModel,Field
from app.models.plan import AgentType
class ReviewResult(BaseModel):
    passed:bool
    confidence: float = Field(ge=0.0, le=1.0)
    feedback: str
    issues: list[str]=Field(default_factory=list)
    next_action: AgentType
    retry_task: str | None = None