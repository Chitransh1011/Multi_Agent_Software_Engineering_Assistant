from fastapi import Depends,APIRouter
from app.api.dependencies import get_graph_service
from app.api.llm_schemas import GenerateRequest
from app.graph.langgraph_service import LangGraphService
from app.graph.state import AgentState
from app.utils.logging import logger

router = APIRouter()

@router.post("/generate",response_model=AgentState)
async def generate(request : GenerateRequest,graph:LangGraphService = Depends(get_graph_service)):

    
    state = await graph.execute(request.user_query)
    return state
