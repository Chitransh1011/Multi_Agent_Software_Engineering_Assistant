from sqlalchemy.orm import Session
from app.db.repositories.artifact_repository import ArtifactRepository
from app.db.repositories.conversation_repository import ConversationRepository
from app.db.repositories.execution_history_repository import ExecutionHistoryRepository
from app.db.repositories.message_repository import MessageRepository


class UnitOfWork:

    def __init__(self, db: Session):
        self.conversations = ConversationRepository(db)
        self.artifacts = ArtifactRepository(db)
        self.messages = MessageRepository(db)
        self.execution = ExecutionHistoryRepository(db)