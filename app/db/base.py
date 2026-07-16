from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

from app.db.models.conversation import Conversation
from app.db.models.artifact import Artifact
from app.db.models.execution_history import ExecutionHistory
from app.db.models.message import Message