from pydantic import BaseModel

class LLMResponse(BaseModel):
    content : str
    model : str
    prompt_tokens : int
    completion_tokens : int
    total_tokens : int
    finish_reason : str
    latency_ms : float
