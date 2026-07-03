from .base_agent import BaseAgent
from app.prompts.planner import PLANNER_SYSTEM_PROMPT
from app.api.schemas import Message
from app.models.plan import Plan
from app.services.llm_service import LLMService
from app.graph.state import AgentState
class PlannerAgent(BaseAgent):
    def __init__(self,llm_service:LLMService,model:str="gpt-4o-mini"):
        super().__init__(llm_service=llm_service,model=model,response_model=Plan)
      

    def _build_prompt(self, state)-> list[Message]:
        
        system_message = Message(role="system",content=PLANNER_SYSTEM_PROMPT)
        user_message = Message(role="user",content=state.user_query)
        return [
            system_message,
            user_message
        ]
    def _update_state(self, state, response)-> AgentState:
        state.plan = response
        state.current_step_index = 0
        return state