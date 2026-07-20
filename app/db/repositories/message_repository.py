from sqlalchemy.orm import Session
from app.db.models.message import Message
from uuid import UUID
from sqlalchemy import select,func

class MessageRepository:

    def __init__(self,db:Session):
        self.db = db

    def add(self,message:Message)->Message:

        self.db.add(message)
        return message
    
    def get(self,message_id:UUID)->Message|None:
        return (
            self.db.query(Message).filter(Message.id == message_id).first()
        )

    def delete(self,message:Message):
        self.db.delete(message)

    def list_by_conversation(
        self,
        conversation_id: UUID,
    ) -> list[Message]:
        return (
            self.db.execute(
                select(Message)
                .where(
                    Message.conversation_id == conversation_id
                )
                .order_by(Message.created_at)
            )
            .scalars()
            .all()
        )
    
    def count(self) -> int:
        return self.db.scalar(
            select(func.count(Message.id))
        ) or 0