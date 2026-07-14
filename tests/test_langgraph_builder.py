from datetime import datetime
from app.models.review import ReviewResult
from app.graph.langgraph_builder import (
    LangGraphBuilder,
    RESEARCH_NODE,
    CODING_NODE,
    REVIEW_NODE,
    WRITER_NODE,
)

from app.graph.state import AgentState
from app.models.plan import Plan, PlanStep, AgentType

class DummyAgent:
    async def run(self, state, task=None):
        return state

def create_builder():

    dummy = DummyAgent()

    return LangGraphBuilder(
        planner=dummy,
        research=dummy,
        coding=dummy,
        review=dummy,
        writer=dummy,
    )


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

def test_route_after_planner_without_research():

    builder = create_builder()

    state = create_state()

    state.plan.needs_research = False

    assert (
        builder.route_after_planner(state)
        == CODING_NODE
    )

def test_route_after_planner_with_research():

    builder = create_builder()

    state = create_state()

    state.plan.needs_research = True

    assert (
        builder.route_after_planner(state)
        == RESEARCH_NODE
    )

def test_route_after_coding_continue():

    builder = create_builder()

    state = create_state()

    state.current_step_index = 1

    assert (
        builder.route_after_coding(state)
        == CODING_NODE
    )

def test_route_after_coding_review():

    builder = create_builder()

    state = create_state()

    state.current_step_index = 2

    assert (
        builder.route_after_coding(state)
        == REVIEW_NODE
    )

def test_route_after_review_passed():

    builder = create_builder()

    state = create_state()

    state.review_result = ReviewResult(
        passed=True,
        confidence=1.0,
        feedback="Good",
        issues=[],
        retry_task=None,
        next_action=AgentType.WRITER,
    )

    assert (
        builder.route_after_review(state)
        == WRITER_NODE
    )

def test_route_after_review_failed():

    builder = create_builder()

    state = create_state()

    state.review_result = ReviewResult(
        passed=False,
        confidence=0.6,
        feedback="Fix it",
        issues=["issue"],
        retry_task="Fix html",
        next_action=AgentType.CODING,
    )

    assert (
        builder.route_after_review(state)
        == CODING_NODE
    )

def test_retry_limit():

    builder = create_builder()

    state = create_state()

    state.retry_attempts = 3

    state.review_result = ReviewResult(
        passed=False,
        confidence=0.5,
        feedback="Still failing",
        issues=["issue"],
        retry_task="Retry",
        next_action=AgentType.CODING,
    )

    assert (
        builder.route_after_review(state)
        == WRITER_NODE
    )