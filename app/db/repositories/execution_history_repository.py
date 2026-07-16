from sqlalchemy.orm import Session
from app.db.models.execution_history import ExecutionHistory
from uuid import UUID

class ExecutionHistoryRepository:

    def __init__(self,db:Session):
        self.db = db

    def create(self,executionhistory:ExecutionHistory)->ExecutionHistory:

        self.db.add(executionhistory)
        self.db.commit()
        self.db.refresh(executionhistory)

        return executionhistory
    
    def get(self,executionhistory_id:UUID)->ExecutionHistory|None:
        return (
            self.db.query(ExecutionHistory).filter(ExecutionHistory.id == executionhistory_id).first()
        )

    def update(self,executionhistory:ExecutionHistory):
        self.db.commit()
        self.db.refresh(executionhistory)

    def delete(self,executionhistory:ExecutionHistory):
        self.db.delete(executionhistory)
        self.db.commit()