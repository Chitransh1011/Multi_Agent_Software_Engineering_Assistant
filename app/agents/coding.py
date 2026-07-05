from app.agents.base_agent import BaseAgent
from app.services.llm_service import LLMService
from app.api.schemas import Message
from app.models.coding import CodingResult
from app.prompts.coding import CODING_SYSTEM_PROMPT
from app.models.generated_artifcats import Generated_Artifact
class CodingAgent(BaseAgent):

    def __init__(self, llm_service:LLMService, model:str="gpt-4o-mini"):
        super().__init__(llm_service=llm_service, model=model, response_model=CodingResult)

    def _build_prompt(self, state, task = None)->list[Message]:
        system_message = Message(
            role="system",
            content=CODING_SYSTEM_PROMPT
        )
        user_content = f"""
            Original user query : 
            {state.user_query}
            Task is : 
            {task}
            Retrieved Context : 
            {state.retrieved_context or "No additional context available."}
        """
        user_message = Message(
            role="user",
            content=user_content
        )
        return [
            system_message,user_message
        ]
        
    def _update_state(self, state, response, task = None):
        
        state.generated_artifacts.append(
            Generated_Artifact(
                artifact_type="python",
                task=task,
                content=response.content,
                filename=response.filename
            )
        )
        print(len(state.generated_artifacts))
        for artifact in state.generated_artifacts:
            print(artifact.filename)
        
        return state
