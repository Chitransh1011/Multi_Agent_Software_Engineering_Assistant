from pydantic import BaseModel


class Generated_Artifact(BaseModel):
    filename: str
    artifact_type: str
    description: str
    content: str