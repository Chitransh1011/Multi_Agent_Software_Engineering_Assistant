from sqlalchemy.orm import Session
from app.db.models.conversation import Conversation
from uuid import UUID
class ConversationRepository:

    def __init__(self,db:Session):
        self.db = db

    def create(self,conversation:Conversation)->Conversation:

        self.db.add(conversation)
        self.db.commit()
        self.db.refresh(conversation)

        return conversation
    
    def get(self,conversation_id:UUID)->Conversation|None:
        return (
            self.db.query(Conversation).filter(Conversation.id == conversation_id).first()
        )

    def update(self,conversation:Conversation):
        self.db.commit()
        self.db.refresh(conversation)

    def delete(self,conversation:Conversation):
        self.db.delete(conversation)
        self.db.commit()
        