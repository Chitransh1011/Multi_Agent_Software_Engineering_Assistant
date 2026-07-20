from sqlalchemy.orm import Session
from app.db.models.execution_history import ExecutionHistory
from uuid import UUID
from sqlalchemy import select,func

class ExecutionHistoryRepository:

    def __init__(self,db:Session):
        self.db = db

    def add(self,executionhistory:ExecutionHistory)->ExecutionHistory:

        self.db.add(executionhistory)
        return executionhistory
    
    def get(self,executionhistory_id:UUID)->ExecutionHistory|None:
        return (
            self.db.query(ExecutionHistory).filter(ExecutionHistory.id == executionhistory_id).first()
        )


    def delete(self,executionhistory:ExecutionHistory):
        self.db.delete(executionhistory)



    def list_by_conversation(
        self,
        conversation_id: UUID,
    ) -> list[ExecutionHistory]:
        return (
            self.db.execute(
                select(ExecutionHistory)
                .where(
                    ExecutionHistory.conversation_id == conversation_id
                )
                .order_by(ExecutionHistory.started_at)
            )
            .scalars()
            .all()
        )
    
    def average_latency(self) -> float:

        stmt = select(
            func.avg(ExecutionHistory.latency_ms)
        )

        return self.db.scalar(stmt) or 0.0