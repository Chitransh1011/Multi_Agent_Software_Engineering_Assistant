from app.graph.langgraph_builder import LangGraphBuilder
from app.graph.state import AgentState
from datetime import datetime

from app.db.models.conversation import Conversation,ConversationStatus
from app.db.models.execution_history import ExecutionHistory
from app.db.repositories.unit_of_work import UnitOfWork
from app.utils.logging import logger
from app.db.models.artifact import Artifact
from app.db.models.message import Message
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
            state = AgentState.model_validate(result)
            
            conversation.status = ConversationStatus.COMPLETED
            logger.info(
                "[%s] Persisting %d execution steps",
                state.request_id,
                len(state.execution_history),
            )
            for step in state.execution_history:
                self.uow.execution.create(
                    ExecutionHistory(
                        conversation_id = state.conversation_id,
                        agent_name = step.agent_name,
                        started_at = step.started_at,
                        ended_at = step.ended_at,
                        latency_ms = step.latency_ms,
                        status = step.status,
                    )
                )
            logger.info(
                "[%s] Execution history saved",
                state.request_id,
            )
            logger.info(
                "[%s] Persisting %d artifacts",
                state.request_id,
                len(state.generated_artifacts),
            )

            for artifact in state.generated_artifacts:
                self.uow.artifacts.create(
                    Artifact(
                        conversation_id=state.conversation_id,
                        filename=artifact.filename,
                        artifact_type=artifact.artifact_type,
                        description=artifact.description,
                        content=artifact.content,
                    )
                )

            logger.info(
                "[%s] Artifacts persisted",
                state.request_id,
            )
            logger.info(
                "[%s] Persisting %d messages",
                state.request_id,
                len(state.agent_messages),
            )

            for message in state.agent_messages:
                self.uow.messages.create(
                    Message(
                        conversation_id=state.conversation_id,
                        role=message.role,
                        content=message.content,
                        agent_name=message.agent_name
                    )
                )
            logger.info(
                "Agent messages collected: %d",
                len(state.agent_messages),
            )
            logger.info(
                "[%s] Messages persisted",
                state.request_id,
            )            
            logger.info(
            "Final execution history length = %d",
            len(state.execution_history),
        )
        except Exception:
            conversation.status = ConversationStatus.FAILED  
            raise
        finally:
            conversation.updated_at = datetime.now()
            self.uow.conversations.update(conversation)

        return state