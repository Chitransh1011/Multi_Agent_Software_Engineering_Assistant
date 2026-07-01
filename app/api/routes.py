from app.services.llm_service import LLMService
from fastapi import Depends,APIRouter
from app.api.dependencies import get_llm_service
from app.models.llm_response import LLMResponse
from app.api.schemas import GenerateRequest

router = APIRouter()

@router.post("/generate",response_model=LLMResponse)
async def generate(request : GenerateRequest,llm:LLMService = Depends(get_llm_service)):


    response = await llm.generate(
        messages=request.messages,
        model=request.model,
        temperature=request.temperature
    )
    return response
