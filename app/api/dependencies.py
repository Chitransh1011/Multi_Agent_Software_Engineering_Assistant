from app.services.llm_service import LLMService
from app.config.config import settings
from app.graph.graph import GraphService
from app.agents.planner import PlannerAgent


llm_service = LLMService(settings=settings)
planner_agent = PlannerAgent(llm_service=llm_service)
graph_service = GraphService(planner=planner_agent)


def get_llm_service():
    return llm_service

def get_graph_service():
    return graph_service