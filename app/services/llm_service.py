from app.models.llm_response import LLMResponse
from app.config.config import Settings
from app.api.schemas import Message
from openai import AsyncOpenAI
import time
from typing import TypeVar
from pydantic import BaseModel


T = TypeVar("T", bound=BaseModel)
class LLMService:
    def __init__(self,settings:Settings):
        self.settings = settings
        self.client = AsyncOpenAI(api_key=settings.openai_api_key)

    async def generate(self,messages:list[Message],response_model:type[T]|None=None,model:str|None=None,temperature:float=0.2) -> T| LLMResponse:
        try:       
            formatted_message = [
                message.model_dump() for message in messages
            ]
            start = time.perf_counter()
            selected_model = model or self.settings.DEFAULT_MODEL
            if response_model is None:
                response = await self.client.chat.completions.create(
                    model=selected_model,
                    messages = formatted_message,
                    temperature=temperature
                )
            else:
                response = await self.client.beta.chat.completions.parse(
                    model=selected_model,
                    messages = formatted_message,
                    temperature=temperature,
                    response_format=response_model
                )
            if response.choices[0].finish_reason!="stop":
                raise RuntimeError("Problem has occured")
            end = time.perf_counter()
            latency = (end-start)*1000
            if response_model is not None:
                return response.choices[0].message.parsed
            
            return self._map_response(response,model=selected_model,latency=latency)
            
        except Exception:
            raise
    def _map_response(self,response,model,latency) -> LLMResponse:
        result = response.choices[0].message.content
        prompt_tokens = response.usage.prompt_tokens
        completion_tokens = response.usage.completion_tokens
        total_tokens = response.usage.total_tokens
        finish_reason = response.choices[0].finish_reason

        return LLMResponse(
            content=result,
            model=model,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=total_tokens,
            finish_reason=finish_reason,
            latency_ms=latency
        )

    

