from pydantic import BaseModel
from datetime import datetime
from enum import Enum

class AgentStatus(Enum):
    SUCCESS = "success"
    FAILED = "failed"
    RUNNING = "running"

class ExecutionStep(BaseModel):
    agent_name: str
    started_at: datetime
    ended_at : datetime
    latency_ms : float
    status: AgentStatus

