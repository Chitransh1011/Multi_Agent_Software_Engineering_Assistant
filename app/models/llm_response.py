from pydantic import BaseModel

class LLMResponse(BaseModel):
    content : str
    model : str
    prompt_token : int
    completition_token : int
    total_token : int
    finish_reason : str
    latency_ms : float
