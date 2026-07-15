import uuid
from sqlalchemy import DateTime,Text
from sqlalchemy.orm import Mapped,mapped_column
from sqlalchemy.sql import func
from app.db.base import Base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Enum
import enum

class ConversationStatus(enum.Enum):
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class Conversation(Base):
    __tablename__ = "conversations"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    request_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        unique=True,
        nullable=False,
    )

    user_query: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    status: Mapped[ConversationStatus] = mapped_column(
        Enum(ConversationStatus),
        default=ConversationStatus.RUNNING,
        nullable=False,
    )
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )