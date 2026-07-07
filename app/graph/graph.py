from app.agents.planner import PlannerAgent
from app.graph.state import AgentState,AgentType
from datetime import datetime
from app.agents.coding import CodingAgent
from app.config.config import settings
from app.agents.review import ReviewAgent
from app.agents.writer import WriterAgent
from app.agents.base_agent import BaseAgent
from app.models.plan import Plan
from app.models.execution_plan import ExecutionPlan
class GraphService:
    def __init__(self,planner:PlannerAgent,coding:CodingAgent,review:ReviewAgent,writer:WriterAgent):
        self.planner = planner
        self.writer = writer
        self.agents:dict[AgentType,BaseAgent] = {
            AgentType.CODING:coding,
            AgentType.REVIEW:review,
        }
    def _create_initial_state(self,user_query:str)->AgentState:
        now = datetime.now()
        state = AgentState(
            user_query=user_query,
            messages=[],
            created_at=now,
            updated_at=now,
            current_step_index=0,
            current_agent=None
        )
        return state

    async def _run_planner(self,state)->AgentState:
        state = await self.planner.run(state=state)
        if state.plan is None:
            raise RuntimeError("Planner did not return a plan")
        return state
    
    async def _run_agent(self,state:AgentState,agent_type:AgentType,task:str|None=None)->AgentState:
        return await self.agents[agent_type].run(state=state,task=task)
    
    async def _run_coding_steps(self,state,coding_steps)->AgentState:
        for step in coding_steps:
            state = await self._run_agent(state,AgentType.CODING, task=step.task)
        return state

    async def _run_review_loop(self,state,review_step)->AgentState:
        while True:
            state = await self._run_agent(state,AgentType.REVIEW, task=review_step.task)
            if state.review_result.passed:
                break

            state.retry_attempts += 1

            if state.retry_attempts >= settings.MAX_RETRIES:
                raise RuntimeError(f"Maximum retries ({settings.MAX_RETRIES}) reached.")

            state = await self._run_agent(
                state,
                agent_type=AgentType.CODING,
                task=state.review_result.retry_task,
            )
        return state

    async def _run_writer(self,state)->AgentState:
        return await self.writer.run(state)
    
    def _extract_execution_plan(self,plan: Plan)->ExecutionPlan:
        coding_steps = [
            step 
            for step in plan.steps 
            if step.agent==AgentType.CODING]
        review_step = next(
            (
                step
                for step in plan.steps
                if step.agent == AgentType.REVIEW
            ),None,)
        
        if review_step is None:
            raise RuntimeError("Planner did not create a review step.")
        return ExecutionPlan(coding_steps=coding_steps,review_step=review_step)

    async def execute(self,user_query:str) -> AgentState :

        state = self._create_initial_state(user_query)
        state = await self._run_planner(state=state)
        execution_plan = self._extract_execution_plan(state.plan)
        state = await self._run_coding_steps(state, execution_plan.coding_steps)
        state = await self._run_review_loop(state, execution_plan.review_step)
        state = await self._run_writer(state)
        return state

