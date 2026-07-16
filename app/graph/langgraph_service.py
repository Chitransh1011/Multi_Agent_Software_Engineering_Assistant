from app.graph.langgraph_builder import LangGraphBuilder
from app.graph.state import AgentState
from datetime import datetime
from app.db.repositories.conversation_repository import ConversationRepository
from app.db.models.conversation import Conversation,ConversationStatus
from app.db.repositories.unit_of_work import UnitOfWork
from app.utils.logging import logger
class LangGraphService:

    def __init__(self,builder:LangGraphBuilder,unit_of_work:UnitOfWork):
        self.graph = builder.build()
        self.uow = unit_of_work
    

    def _create_initial_state(self,user_query:str)->AgentState:
        now = datetime.now()
        return AgentState(
            user_query=user_query,
            messages=[],
            workflow_started_at=now,
            created_at=now,
            updated_at=now,
            current_step_index=0,
            current_agent=None
        )
    
    async def execute(self,user_query: str) -> AgentState:

        state = self._create_initial_state(user_query)
        logger.info(
            "[%s] Creating conversation",
            state.request_id,
        )
        conversation = self.uow.conversations.create(
            Conversation(
                request_id = state.request_id,
                user_query = user_query,
                status = ConversationStatus.RUNNING
            )
        )
        logger.info(
            "[%s] Conversation %s created",
            state.request_id,
            conversation.id,
        )
        state.conversation_id = conversation.id
        
        try:
            result = await self.graph.ainvoke(state)
            conversation.status = ConversationStatus.COMPLETED
        except Exception:
            conversation.status = ConversationStatus.FAILED  
            raise
        finally:
            conversation.updated_at = datetime.now()
            self.uow.conversations.update(conversation)

        return AgentState.model_validate(result)