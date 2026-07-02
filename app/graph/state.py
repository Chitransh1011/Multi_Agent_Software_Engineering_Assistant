from pydantic import BaseModel,Field
from .execution import ExecutionStep
from app.api.schemas import Message
from typing import Any
from datetime import datetime


class AgentState(BaseModel):
    user_query: str
    messages: list[Message] = Field(default_factory=list)
    execution_history: list[ExecutionStep] = Field(default_factory=list)
    current_agent: str
    metadata: dict[str,Any] = Field(default_factory=dict)
    timestamp: datetime
    planner_response: str | None = None
    research_response: str | None = None
    coding_response: str | None = None
    review_response: str | None = None
    review_passed: bool | None = None
    final_response: str | None = None
    retry_attempts : int = 0
    errors : list[str] = Field(default_factory=list)
    created_at: datetime
    updated_at: datetime


