from uuid import UUID

from fastapi import HTTPException, status
from app.db.models.conversation import ConversationStatus
import math

from app.api.schema.conversation import (
    ConversationDetailResponse,
    ConversationListResponse,
    ConversationResponse,
    ExecutionHistoryResponse,
    ArtifactResponse,
    MessageResponse,
    PaginationResponse
)
from app.db.repositories.unit_of_work import UnitOfWork


class ConversationService:

    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    def list_conversations(
        self,
        *,
        page: int = 1,
        page_size: int = 10,
        status: ConversationStatus | None = None,
        query: str | None = None,
    ) -> ConversationListResponse:

        conversations = self.uow.conversations.list(
            page=page,
            page_size=page_size,
            status=status,
            query=query,
        )

        total = self.uow.conversations.count(
            status=status,
            query=query,
        )

        total_pages = math.ceil(total / page_size) if total else 0

        return ConversationListResponse(
            conversations=[
                ConversationResponse.model_validate(c)
                for c in conversations
            ],
            pagination=PaginationResponse(
                page=page,
                page_size=page_size,
                total_items=total,
                total_pages=total_pages,
                has_next=page < total_pages,
                has_previous=page > 1,
            ),
        )
    
    def get_conversation(
        self,
        conversation_id: UUID,
    ) -> ConversationDetailResponse:
        
        conversation = self.uow.conversations.get(conversation_id)

        if conversation is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found",
            )
        
        messages = self.uow.messages.list_by_conversation(
            conversation_id
        )

        artifacts = self.uow.artifacts.list_by_conversation(
            conversation_id
        )

        execution = self.uow.execution.list_by_conversation(
            conversation_id
        )

        return ConversationDetailResponse(
            conversation=ConversationResponse.model_validate(
                conversation
            ),
            execution_history=[
                ExecutionHistoryResponse.model_validate(e)
                for e in execution
            ],
            artifacts=[
                ArtifactResponse.model_validate(a)
                for a in artifacts
            ],
            messages=[
                MessageResponse.model_validate(m)
                for m in messages
            ],
        )
    
    def delete_conversation(
        self,
        conversation_id: UUID,
    ):
        conversation = self.uow.conversations.get(conversation_id)

        if conversation is None:
            raise HTTPException(
                status_code=404,
                detail="Conversation not found",
            )

        self.uow.conversations.delete(conversation)

        self.uow.commit()