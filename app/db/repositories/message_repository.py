from sqlalchemy.orm import Session
from app.db.models.message import Message
from uuid import UUID

class MessageRepository:

    def __init__(self,db:Session):
        self.db = db

    def create(self,message:Message)->Message:

        self.db.add(message)
        self.db.commit()
        self.db.refresh(message)

        return message
    
    def get(self,message_id:UUID)->Message|None:
        return (
            self.db.query(Message).filter(Message.id == message_id).first()
        )

    def update(self,message:Message):
        self.db.commit()
        self.db.refresh(message)

    def delete(self,message:Message):
        self.db.delete(message)
        self.db.commit()