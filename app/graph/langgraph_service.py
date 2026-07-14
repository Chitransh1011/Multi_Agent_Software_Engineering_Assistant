from app.graph.langgraph_builder import LangGraphBuilder
from app.graph.state import AgentState
from datetime import datetime


class LangGraphService:

    def __init__(self,builder:LangGraphBuilder):
        self.graph = builder.build()
    

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

        result = await self.graph.ainvoke(state)

        return AgentState.model_validate(result)