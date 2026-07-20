from datetime import datetime
from uuid import UUID

from pydantic import BaseModel
from app.db.models.conversation import Conversation
from app.db.models.execution_history import ExecutionHistory
from app.db.models.artifact import Artifact
from app.db.models.message import Message
from app.db.models.conversation import ConversationStatus
from app.graph.execution import AgentStatus
from sqlalchemy import func, select


class ConversationResponse(BaseModel):
    id: UUID
    request_id: UUID
    user_query: str
    status: ConversationStatus
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }


class ExecutionHistoryResponse(BaseModel):
    agent_name: str
    started_at: datetime
    ended_at: datetime
    latency_ms: float
    status: AgentStatus

    model_config = {
        "from_attributes": True
    }
        


class ArtifactResponse(BaseModel):
    filename: str
    artifact_type: str
    description: str
    content: str

    model_config = {
        "from_attributes": True
    }


class MessageResponse(BaseModel):
    role: str
    content: str
    agent_name: str

    model_config = {
        "from_attributes": True
    }


class ConversationDetailResponse(BaseModel):
    conversation: ConversationResponse
    execution_history: list[ExecutionHistoryResponse]
    artifacts: list[ArtifactResponse]
    messages: list[MessageResponse]

class PaginationResponse(BaseModel):
    page: int
    page_size: int
    total_items: int
    total_pages: int
    has_next: bool
    has_previous: bool

class ConversationListResponse(BaseModel):
    conversations: list[ConversationResponse]
    pagination: PaginationResponse

