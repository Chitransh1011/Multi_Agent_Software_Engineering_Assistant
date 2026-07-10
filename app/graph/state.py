from pydantic import BaseModel,Field
from .execution import ExecutionStep
from app.api.schemas import Message
from typing import Any
from datetime import datetime
from app.models.plan import AgentType
from app.models.generated_artifcats import Generated_Artifact
from app.models.plan import Plan,PlanStep
from app.models.review import ReviewResult
from app.models.writer import WriterResult
from app.models.research import ResearchResult
class AgentState(BaseModel):
    user_query: str
    messages: list[Message] = Field(default_factory=list)
    execution_history: list[ExecutionStep] = Field(default_factory=list)
    current_agent: AgentType | None=None
    metadata: dict[str,Any] = Field(default_factory=dict)
    plan: Plan | None = None
    research_result: ResearchResult | None = None
    generated_artifacts: list[Generated_Artifact] = Field(default_factory=list)
    review_result: ReviewResult | None = None
    final_response: WriterResult | None = None
    retry_attempts : int = 0
    errors : list[str] = Field(default_factory=list)
    created_at: datetime
    updated_at: datetime
    current_step_index: int

    def get_coding_steps(self)->list[PlanStep]:
        if self.plan is None:
            return []

        return [
            step
            for step in self.plan.steps
            if step.agent == AgentType.CODING
        ]

    def coding_step_count(self) -> int:
        return len(self.get_coding_steps())
    
    def get_current_task(self) -> str | None:
        coding_steps = self.get_coding_steps()

        if self.current_step_index >= len(coding_steps):
            return None

        return coding_steps[self.current_step_index].task
    
    def get_artifact(
    self,
    filename: str,
    ) -> Generated_Artifact | None:
        for artifact in self.generated_artifacts:
            if artifact.filename == filename:
                return artifact
        return None


    def upsert_artifact(
        self,
        artifact: Generated_Artifact,
    ) -> None:
        for existing in self.generated_artifacts:
            if existing.filename == artifact.filename:
                existing.content = artifact.content
                existing.task = artifact.task
                existing.artifact_type = artifact.artifact_type
                return

        self.generated_artifacts.append(artifact)



