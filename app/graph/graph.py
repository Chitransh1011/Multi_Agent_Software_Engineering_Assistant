from app.agents.planner import PlannerAgent
from app.graph.state import AgentState
from datetime import datetime
class GraphService:
    def __init__(self,planner:PlannerAgent):
        self.planner = planner

    async def execute(self,user_query:str) -> AgentState :
        now = datetime.now()
        state = AgentState(
            user_query=user_query,
            messages=[],
            created_at=now,
            updated_at=now,
            current_step_index=0,
            current_agent=None
        )
        state = await self.planner.run(state)

        return state

