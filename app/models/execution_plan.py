from app.models.plan import PlanStep
from pydantic import BaseModel

class ExecutionPlan(BaseModel):

    coding_steps: list[PlanStep]

    review_step: PlanStep