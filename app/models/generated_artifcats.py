from pydantic import BaseModel


class Generated_Artifact(BaseModel):
    artifact_type:str
    task:str
    content:str
    filename:str