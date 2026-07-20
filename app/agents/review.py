from app.agents.base_agent import BaseAgent
from app.models.review import ReviewResult
from app.services.llm_service import LLMService
from app.api.llm_schemas import Message
from app.prompts.review import REVIEW_SYSTEM_PROMPT
from app.graph.state import AgentState
from app.utils.logging import logger
class ReviewAgent(BaseAgent):
    def __init__(self, llm_service:LLMService, model = "gpt-4o-mini"):
        super().__init__(llm_service=llm_service, model=model, response_model=ReviewResult)
    

    def _build_prompt(self, state, task )->list[Message]:
        
        system_message = Message(
            role = "system",
            content = REVIEW_SYSTEM_PROMPT
        )
        artifacts = ""
        for artifact in state.generated_artifacts:
            artifacts += f"""
            Filename : {artifact.filename}

            Type:
            {artifact.artifact_type}

            Content:
            {artifact.content}

            ----------------------
           """
        
        previous_feedback = (
            state.review_result.feedback
            if state.review_result
            else "No previous review."
        )
        user_content = f"""
            Original User Request : 
            {state.user_query}

            Generated Artifacts :
            {artifacts}

            Review Task : 
            {task}
            Previous review:
            {previous_feedback}

            Retry attempt:
            {state.retry_attempts}

        """
        user_message = Message(
            role="user",
            content=user_content
        )
        return [
            system_message,user_message
        ]
    
    def _update_state(self, state, response, task)->AgentState:
        state.review_result = response
        logger.info(
            "Review confidence: %.2f",
            response.confidence,
        )
        return state
    