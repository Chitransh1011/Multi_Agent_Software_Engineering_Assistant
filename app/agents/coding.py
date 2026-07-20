from app.agents.base_agent import BaseAgent
from app.services.llm_service import LLMService
from app.api.llm_schemas import Message
from app.models.coding import CodingResult
from app.prompts.coding import CODING_SYSTEM_PROMPT
from app.models.generated_artifcats import Generated_Artifact
from app.utils.logging import logger
class CodingAgent(BaseAgent):

    def __init__(self, llm_service:LLMService, model:str="gpt-4o-mini"):
        super().__init__(llm_service=llm_service, model=model, response_model=CodingResult)

    def _build_prompt(self, state, task = None)->list[Message]:
        system_message = Message(
            role="system",
            content=CODING_SYSTEM_PROMPT
        )
        review_feedback = (
            state.review_result.feedback
            if state.review_result
            else "No review feedback available."
        )

        issues = (
            "\n".join(state.review_result.issues)
            if state.review_result
            else "No issues reported."
        )
        research_summary = (
            state.research_result.summary
            if state.research_result
            else "No research available"
        )
        artifacts = ""
        for artifact in state.generated_artifacts:
            artifacts += f"""
                Filename : 
                {artifact.filename}

                Type : 
                {artifact.artifact_type}

                Content :
                {artifact.content}

                -----------------------
            """
        user_content = f"""
            Original user query : 
            {state.user_query}

            Task is : 
            {task}

            Retrieved Context : 
            {research_summary}

            REVIEW FEEDBACK:
            {review_feedback}

            ISSUES:
            {issues}
            
            Current Project Files : 
            {artifacts}
        """
        user_message = Message(
            role="user",
            content=user_content
        )
        return [
            system_message,user_message
        ]
        
    def _update_state(self, state, response, task = None):
        
        state.upsert_artifact(
            Generated_Artifact(
                artifact_type=response.artifact_type,
                description=task,
                content=response.content,
                filename=response.filename
            )
        )
        logger.info(
            "Generated artifact: %s",
            response.filename,
        )
            
        
        state.review_result = None
        return state
