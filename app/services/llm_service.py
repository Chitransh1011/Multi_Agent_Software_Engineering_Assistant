from app.models.llm_response import LLMResponse
from app.config.config import settings,Settings
from app.api.schemas import Message
from openai import AsyncOpenAI
import time



class LLMService:
    def __init__(self,settings:Settings):
        self.settings = settings
        self.client = AsyncOpenAI(api_key=settings.openai_api_key)

    async def generate(self,messages:list[Message],model:str|None=None,temperature:float=0.2) -> LLMResponse:
        try:       
            formatted_message = [
                message.model_dump() for message in messages
            ]
            start = time.perf_counter()
            selected_model = model or self.settings.DEFAULT_MODEL
            response = await self.client.beta.chat.completions.parse(
                model=selected_model,
                messages = formatted_message,
                response_format=LLMResponse,
                temperature=temperature
            )
            end = time.perf_counter()
            latency = (end-start)*1000

            result = response.choices[0].message.content
            prompt_token = response.usage.prompt_tokens
            completion_token = response.usage.completion_tokens
            total_token = response.usage.total_tokens
            finish_reason = response.choices[0].finish_reason


            return LLMResponse(
                content=result,
                model=selected_model,
                prompt_token=prompt_token,
                completition_token=completion_token,
                total_token=total_token,
                finish_reason=finish_reason,
                latency_ms=latency
            )
        except Exception:
            raise
    
    

