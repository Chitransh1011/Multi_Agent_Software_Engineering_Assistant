from datetime import datetime, UTC
from uuid import uuid4

from fastapi import HTTPException

from app.api.schema.conversation import (
    ConversationListResponse,
    ConversationDetailResponse,
    ConversationResponse,
    PaginationResponse,
    MessageResponse,
    ArtifactResponse,
    ExecutionHistoryResponse,
    AgentStatus,
)


def test_list_conversations(
    client,
    mock_conversation_service,
):
    response_model = ConversationListResponse(
        conversations=[
            ConversationResponse(
                id=uuid4(),
                request_id=uuid4(),
                user_query="Generate Login API",
                status="completed",
                created_at=datetime.now(UTC),
                updated_at=datetime.now(UTC),
            )
        ],
        pagination=PaginationResponse(
            page=1,
            page_size=10,
            total_items=1,
            total_pages=1,
            has_next=False,
            has_previous=False,
        ),
    )

    mock_conversation_service.list_conversations.return_value = response_model

    response = client.get("/api/v1/conversations")

    assert response.status_code == 200
    assert len(response.json()["conversations"]) == 1

    mock_conversation_service.list_conversations.assert_called_once()


def test_list_empty(
    client,
    mock_conversation_service,
):
    mock_conversation_service.list_conversations.return_value = (
        ConversationListResponse(
            conversations=[],
            pagination=PaginationResponse(
                page=1,
                page_size=10,
                total_items=0,
                total_pages=0,
                has_next=False,
                has_previous=False,
            ),
        )
    )

    response = client.get("/api/v1/conversations")

    assert response.status_code == 200
    assert response.json()["conversations"] == []


def test_get_conversation(client, mock_conversation_service):

    conversation_id = uuid4()

    response_model = ConversationDetailResponse(
        conversation=ConversationResponse(
            id=conversation_id,
            request_id=uuid4(),
            user_query="Generate Login API",
            status="completed",
            created_at=datetime.now(UTC),
            updated_at=datetime.now(UTC),
        ),
        messages=[
            MessageResponse(
                id=uuid4(),
                conversation_id=conversation_id,
                role="user",
                content="Hello",
                created_at=datetime.now(UTC),
                agent_name="User",
            )
        ],
        artifacts=[
            ArtifactResponse(
                id=uuid4(),
                conversation_id=conversation_id,
                filename="main.py",
                artifact_type="python",
                description="code",
                content="print('hello')",
                created_at=datetime.now(UTC),
            )
        ],
        execution_history=[
            ExecutionHistoryResponse(
                id=uuid4(),
                conversation_id=conversation_id,
                agent_name="Planner",
                status=AgentStatus.SUCCESS,
                latency_ms=100,
                started_at=datetime.now(UTC),
                ended_at=datetime.now(UTC),
                created_at=datetime.now(UTC),
            )
        ],
    )

    mock_conversation_service.get_conversation.return_value = response_model

    response = client.get(
        f"/api/v1/conversations/{conversation_id}"
    )

    assert response.status_code == 200

    assert response.json()["conversation"]["id"] == str(
        conversation_id
    )

    mock_conversation_service.get_conversation.assert_called_once()


def test_get_conversation_not_found(
    client,
    mock_conversation_service,
):

    mock_conversation_service.get_conversation.side_effect = (
        HTTPException(
            status_code=404,
            detail="Conversation not found",
        )
    )

    response = client.get(
        f"/api/v1/conversations/{uuid4()}"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Conversation not found"

def test_delete_conversation(
    client,
    mock_conversation_service,
):

    conversation_id = uuid4()

    response = client.delete(
        f"/api/v1/conversations/{conversation_id}"
    )

    assert response.status_code == 204

    mock_conversation_service.delete_conversation.assert_called_once_with(
        conversation_id
    )

def test_delete_conversation_not_found(
    client,
    mock_conversation_service,
):

    mock_conversation_service.delete_conversation.side_effect = (
        HTTPException(
            status_code=404,
            detail="Conversation not found",
        )
    )

    response = client.delete(
        f"/api/v1/conversations/{uuid4()}"
    )

    assert response.status_code == 404