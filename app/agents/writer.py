from app.agents.base_agent import BaseAgent
from app.models.writer import WriterResult
from app.services.llm_service import LLMService
from app.prompts.writer import WRITER_SYSTEM_PROMPT
from app.api.llm_schemas import Message
from app.graph.state import AgentState
class WriterAgent(BaseAgent):
    def __init__(self, llm_service:LLMService, model = "gpt-4o-mini"):
        super().__init__(llm_service, model, response_model=WriterResult)



    def _build_prompt(self, state, task:str|None=None)->list[Message]:
        
        system_message = Message(
            role="system",
            content=WRITER_SYSTEM_PROMPT
        )

        files = ""
        for artifact in state.generated_artifacts:
            files += f"""
            Filename : {artifact.filename}

            Type: {artifact.artifact_type}


            ----------------------
           """
        user_content = f"""
        Original User Request:
        {state.user_query}

        Generated Files:
        {files}

        Review Result:

        Passed:
        {state.review_result.passed}

        Feedback:
        {state.review_result.feedback}

        Issues:
        {chr(10).join(state.review_result.issues)}
                

        """

        user_message = Message(
            role="user",
            content=user_content
        )
        return [
            system_message,user_message
        ]
    def _update_state(self, state, response, task:str|None=None)->AgentState:
        
        state.final_response = response
        print(state.final_response)
        return state