from datetime import datetime
from app.graph.state import AgentState
from app.models.plan import Plan, PlanStep, AgentType
from app.models.review import ReviewResult
from app.models.generated_artifcats import Generated_Artifact

def create_state():

    plan = Plan(
        needs_research=False,
        reason="Testing",
        steps=[
            PlanStep(
                agent=AgentType.CODING,
                task="Create login.html",
            ),
            PlanStep(
                agent=AgentType.CODING,
                task="Create styles.css",
            ),
        ],
    )

    return AgentState(
        user_query="Create login page",
        created_at=datetime.now(),
        updated_at=datetime.now(),
        current_step_index=0,
        current_agent=None,
        plan=plan,
    )

def test_get_current_task():

    state = create_state()

    assert state.get_current_task() == "Create login.html"

def test_next_task():

    state = create_state()

    state.current_step_index = 1

    assert state.get_current_task() == "Create styles.css"

def test_is_retry_false():

    state = create_state()

    assert state.is_retry() is False

def test_is_retry_true():

    state = create_state()

    state.review_result = ReviewResult(
        passed=False,
        confidence=0.8,
        feedback="Fix",
        issues=[],
        next_action=AgentType.CODING,
        retry_task="Retry",
    )

    assert state.is_retry() is True


def test_upsert_artifact():

    state = create_state()

    artifact = Generated_Artifact(
        filename="login.html",
        artifact_type="HTML",
        description="Login page",
        content="<html></html>",
    )

    state.upsert_artifact(artifact)

    assert len(state.generated_artifacts) == 1


def test_update_existing_artifact():

    state = create_state()

    first = Generated_Artifact(
        filename="login.html",
        artifact_type="HTML",
        description="Task",
        content="old",
    )

    second = Generated_Artifact(
        filename="login.html",
        artifact_type="HTML",
        description="Task",
        content="new",
    )

    state.upsert_artifact(first)
    state.upsert_artifact(second)

    assert len(state.generated_artifacts) == 1

    assert state.generated_artifacts[0].content == "new"