from uuid import UUID

from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy.orm import Session

from app.api.schema.conversation import (
    ConversationListResponse,
    ConversationDetailResponse
)
from app.db.session import get_db
from app.db.repositories.unit_of_work import UnitOfWork
from app.services.conversation_service import ConversationService
from app.db.models.conversation import ConversationStatus


router = APIRouter(
    prefix="/conversations",
    tags=["Conversations"],
)

def get_conversation_service(
    db: Session = Depends(get_db),
) -> ConversationService:
    return ConversationService(UnitOfWork(db))

@router.get(
    "",
    response_model=ConversationListResponse,
    summary="List conversations",
)
def list_conversations(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    status: ConversationStatus | None = None,
    query: str | None = None,
    service: ConversationService = Depends(get_conversation_service),
):
    return service.list_conversations(
        page=page,
        page_size=page_size,
        status=status,
        query=query,
    )

@router.get(
    "/{conversation_id}",
    response_model=ConversationDetailResponse,
    summary="Get conversation details",
)
async def get_conversation(
    conversation_id: UUID,
    service: ConversationService = Depends(get_conversation_service),
):
    return service.get_conversation(conversation_id)

@router.delete(
    "/{conversation_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete conversation",
)
def delete_conversation(
    conversation_id: UUID,
    service: ConversationService = Depends(
        get_conversation_service
    ),
):
    service.delete_conversation(conversation_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)