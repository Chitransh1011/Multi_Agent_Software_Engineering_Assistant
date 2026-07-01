from app.services.llm_service import LLMService
from app.config.config import settings

llm_service = LLMService(settings=settings)

def get_llm_service():
    return llm_service