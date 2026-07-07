from app.agents.base_agent import BaseAgent
from app.models.research import ResearchResult
from app.services.llm_service import LLMService
from app.api.schemas import Message
from app.prompts.research import RESEARCH_SYSTEM_PROMPT
from app.graph.state import AgentState,AgentType

class ResearchAgent(BaseAgent):
    def __init__(self, llm_service:LLMService, model = "gpt-4o-mini"):
        super().__init__(llm_service=llm_service, model=model, response_model=ResearchResult)

    def _build_prompt(self, state, task = None)->list[Message]:
        
        system_messages = Message(
            role="system",
            content=RESEARCH_SYSTEM_PROMPT
        )
        user_content = f"""
        Original Task :
        {state.user_query}

        Research Task :
        {task}

        Current Plan : 
        {state.plan.reason}

        """
        user_message = Message(
            role="user",
            content=user_content
        )
        return [
            system_messages,user_message
        ]
    def _update_state(self, state:AgentState, response:ResearchResult, task = None):
        state.research_result = response
        return state
        