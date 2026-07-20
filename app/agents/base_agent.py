from abc import ABC, abstractmethod
from app.services.llm_service import LLMService
from app.models.llm_response import LLMResponse
from app.api.llm_schemas import Message
from app.graph.state import AgentState
from datetime import datetime
from app.graph.execution import ExecutionStep,AgentStatus
from pydantic import BaseModel
import logging
from app.models.agent_message import AgentMessage

logger = logging.getLogger(__name__)

class BaseAgent(ABC):
    def __init__(self,llm_service :LLMService,model:str|None=None,response_model: type[BaseModel] | None = None):
        self.llm = llm_service
        self.model = model or llm_service.settings.DEFAULT_MODEL
        self.name = self.__class__.__name__
        self.response_model: type[BaseModel] | None = response_model

    def _record_execution(
        self,
        state: AgentState,
        started_at: datetime,
        ended_at: datetime,
        status: AgentStatus,
        error_message: str | None = None,
    ):
        
        latency_ms = (ended_at - started_at).total_seconds() * 1000
        if error_message is not None:
            state.errors.append(error_message)
        state.execution_history.append(ExecutionStep(
            agent_name=self.name,
            started_at=started_at,
            ended_at=ended_at,
            latency_ms=latency_ms,
            status=status
        ))
        
    async def run(self,state:AgentState, task:str|None=None)->AgentState:
        try:
            state.current_agent = self.name
            started_at = datetime.now()

            messages = self._build_prompt(state=state,task=task)

            for message in messages:
                state.agent_messages.append(
                    AgentMessage(
                        agent_name=self.name,
                        role=message.role,
                        content=message.content,
                    )
                )
            logger.info("%s started.", self.name)

            logger.info("%s started.", self.name)
            llm_result = await self._call_llm(messages=messages)
            logger.info("%s completed successfully.", self.name)

            content = (
                llm_result.model_dump_json()
                if isinstance(llm_result, BaseModel)
                else str(llm_result)
            )

            state.agent_messages.append(
                AgentMessage(
                    agent_name=self.name,
                    role="assistant",
                    content=content,
                )
            )

            state = self._update_state(state=state,response=llm_result,task=task)

            ended_at = datetime.now()
            self._record_execution(state,started_at=started_at,ended_at=ended_at,status=AgentStatus.SUCCESS)
            state.current_agent = None
            state.updated_at = ended_at
            return state
        except Exception as e:
            logger.exception("%s failed.", self.name)
            ended_at = datetime.now()
            self._record_execution(state,started_at=started_at,ended_at=ended_at,status=AgentStatus.FAILED,error_message=str(e))
            state.current_agent = None
            state.updated_at = ended_at
            raise

        


    async def _call_llm(self,messages: list[Message])-> BaseModel | LLMResponse:
        response = await self.llm.generate(messages=messages,model=self.model,response_model=self.response_model)
        return response

    @abstractmethod
    def _build_prompt(self,state:AgentState,task:str|None=None)->list[Message]:
        pass

    @abstractmethod
    def _update_state(self,state:AgentState,response,task:str|None=None)->AgentState:
        pass

