from sqlalchemy.orm import Session
from app.db.models.artifact import Artifact
from uuid import UUID
class ArtifactRepository:

    def __init__(self,db:Session):
        self.db = db

    def create(self,artifact:Artifact)->Artifact:

        self.db.add(artifact)
        self.db.commit()
        self.db.refresh(artifact)

        return artifact
    
    def get(self,artifact_id:UUID)->Artifact|None:
        return (
            self.db.query(Artifact).filter(Artifact.id == artifact_id).first()
        )

    def update(self,artifact:Artifact):
        self.db.commit()
        self.db.refresh(artifact)

    def delete(self,artifact:Artifact):
        self.db.delete(artifact)
        self.db.commit()