from pydantic import BaseModel

class StatsResponse(BaseModel):
    total_conversations: int
    completed_conversations: int
    failed_conversations: int
    running_conversations: int

    success_rate: float

    average_latency_ms: float
    average_artifacts_per_conversation: float

    total_messages: int