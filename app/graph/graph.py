from app.agents.planner import PlannerAgent
from app.graph.state import AgentState,AgentType
from datetime import datetime
from app.agents.coding import CodingAgent
from app.agents.research import ResearchAgent
from app.agents.review import ReviewAgent
from app.agents.writer import WriterAgent
from app.agents.base_agent import BaseAgent
class GraphService:
    def __init__(self,planner:PlannerAgent,coding:CodingAgent,review:ReviewAgent,writer:WriterAgent):
        self.planner = planner
        self.writer = writer
        self.agents:dict[AgentType,BaseAgent] = {
            AgentType.CODING:coding,
            AgentType.REVIEW:review,
        }

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
        state = await self.planner.run(state,None)
        if state.plan is None:
            raise RuntimeError("Planner did not return a plan")
        
        print(state.plan.model_dump())
        for step in state.plan.steps:
            try:
                agent = self.agents[step.agent]
            except KeyError:
                raise ValueError(
                    f"No agent registered for {step.agent}"
                )
            state = await agent.run(
                state=state,
                task=step.task
            )
            state.current_step_index += 1
        state = await self.writer.run(state)
        return state

