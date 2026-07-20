from uuid import uuid4
from datetime import datetime, timezone,timedelta

from app.db.models.conversation import Conversation
from app.db.models.execution_history import ExecutionHistory
from app.db.repositories.execution_history_repository import (
    ExecutionHistoryRepository,
)



def create_conversation():
    return Conversation(
        request_id=uuid4(),
        user_query="Test Conversation",
    )


def create_execution_history(
    conversation_id,
    agent_name="Planner",
    status="SUCCESS",
    latency_ms=100.0,
):
    start = datetime.now(timezone.utc)

    return ExecutionHistory(
        conversation_id=conversation_id,
        agent_name=agent_name,
        status=status,
        latency_ms=latency_ms,
        started_at=start,
        ended_at=start + timedelta(milliseconds=latency_ms),
    )


def test_add_and_get_execution_history(db_session):
    conversation = create_conversation()

    db_session.add(conversation)
    db_session.commit()

    repo = ExecutionHistoryRepository(db_session)

    execution = create_execution_history(conversation.id)

    repo.add(execution)
    db_session.commit()

    fetched = repo.get(execution.id)

    assert fetched is not None
    assert fetched.agent_name == "Planner"
    assert fetched.latency_ms == 100.0

def test_get_non_existing_execution_history(db_session):
    repo = ExecutionHistoryRepository(db_session)

    assert repo.get(uuid4()) is None

def test_delete_execution_history(db_session):
    conversation = create_conversation()

    db_session.add(conversation)
    db_session.commit()

    repo = ExecutionHistoryRepository(db_session)

    execution = create_execution_history(conversation.id)

    repo.add(execution)
    db_session.commit()

    repo.delete(execution)
    db_session.commit()

    assert repo.get(execution.id) is None


def test_list_by_conversation(db_session):
    conversation1 = create_conversation()
    conversation2 = create_conversation()

    db_session.add_all([conversation1, conversation2])
    db_session.commit()

    repo = ExecutionHistoryRepository(db_session)

    repo.add(create_execution_history(conversation1.id))
    repo.add(create_execution_history(conversation1.id, latency_ms=200))
    repo.add(create_execution_history(conversation2.id))

    db_session.commit()

    executions = repo.list_by_conversation(conversation1.id)

    assert len(executions) == 2


def test_average_latency(db_session):
    conversation = create_conversation()

    db_session.add(conversation)
    db_session.commit()

    repo = ExecutionHistoryRepository(db_session)

    repo.add(create_execution_history(conversation.id, latency_ms=100))
    repo.add(create_execution_history(conversation.id, latency_ms=200))
    repo.add(create_execution_history(conversation.id, latency_ms=300))

    db_session.commit()

    assert repo.average_latency() == 200.0


def test_average_latency_empty(db_session):
    repo = ExecutionHistoryRepository(db_session)

    assert repo.average_latency() == 0.0