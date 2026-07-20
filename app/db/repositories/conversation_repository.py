from sqlalchemy.orm import Session
from app.db.models.conversation import Conversation
from uuid import UUID
from sqlalchemy import func, select
from app.db.models.conversation import ConversationStatus
class ConversationRepository:

    def __init__(self,db:Session):
        self.db = db

    def add(self,conversation:Conversation)->Conversation:

        self.db.add(conversation)
        return conversation
    
    def get(self,conversation_id:UUID)->Conversation|None:
        return (
            self.db.query(Conversation).filter(Conversation.id == conversation_id).first()
        )


    def delete(self,conversation:Conversation):
        self.db.delete(conversation)
        
    def list(
        self,
        *,
        page: int,
        page_size: int,
        status: ConversationStatus | None = None,
        query: str | None = None,
        ) -> list[Conversation]:

            stmt = select(Conversation)

            if status is not None:
                stmt = stmt.where(Conversation.status == status)

            if query:
                stmt = stmt.where(
                    Conversation.user_query.ilike(f"%{query}%")
                )

            offset = (page - 1) * page_size

            stmt = (
                stmt.order_by(Conversation.created_at.desc())
                .offset(offset)
                .limit(page_size)
            )

            return (
                self.db.execute(stmt)
                .scalars()
                .all()
                )
    def count(
        self,
        *,
        status: ConversationStatus | None = None,
        query: str | None = None,
    ) -> int:

        stmt = select(func.count(Conversation.id))

        if status is not None:
            stmt = stmt.where(
                Conversation.status == status
            )

        if query:
            stmt = stmt.where(
                Conversation.user_query.ilike(f"%{query}%")
            )

        return self.db.scalar(stmt)
    
    def count_by_status(
        self,
        status: ConversationStatus,
    ) -> int:
        stmt = (
            select(func.count(Conversation.id))
            .where(Conversation.status == status)
        )

        return self.db.scalar(stmt) or 0