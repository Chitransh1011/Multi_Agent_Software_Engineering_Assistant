from fastapi import Depends,APIRouter
from app.api.dependencies import get_graph_service
from app.api.schemas import GenerateRequest
from app.graph.graph import GraphService
from app.graph.state import AgentState

router = APIRouter()

@router.post("/generate",response_model=AgentState)
async def generate(request : GenerateRequest,graph:GraphService = Depends(get_graph_service)):


    state = await graph.execute(request.user_query)
    return state
