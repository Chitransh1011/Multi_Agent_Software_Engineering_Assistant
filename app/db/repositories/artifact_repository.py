from sqlalchemy.orm import Session
from app.db.models.artifact import Artifact
from uuid import UUID
from sqlalchemy import select,func
class ArtifactRepository:

    def __init__(self,db:Session):
        self.db = db

    def add(self,artifact:Artifact)->Artifact:

        self.db.add(artifact)
        return artifact
    
    def get(self,artifact_id:UUID)->Artifact|None:
        return (
            self.db.query(Artifact).filter(Artifact.id == artifact_id).first()
        )

    def delete(self,artifact:Artifact):
        self.db.delete(artifact)

    def list_by_conversation(
        self,
        conversation_id: UUID,
    ) -> list[Artifact]:
        return (
            self.db.execute(
                select(Artifact)
                .where(
                    Artifact.conversation_id == conversation_id
                )
            )
            .scalars()
            .all()
        )
    
    def count(self) -> int:
        return self.db.scalar(
            select(func.count(Artifact.id))
        ) or 0
    
    