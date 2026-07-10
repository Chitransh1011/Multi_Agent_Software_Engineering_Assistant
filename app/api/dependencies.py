from app.services.llm_service import LLMService
from app.config.config import settings
from app.graph.graph import GraphService
from app.agents.planner import PlannerAgent
from app.agents.coding import CodingAgent
from app.agents.review import ReviewAgent
from app.agents.writer import WriterAgent
from app.rag.retriever import get_retriever
from app.services.knowledge_service import KnowledgeService
from app.agents.research import ResearchAgent
from app.graph.langgraph_builder import LangGraphBuilder
from app.graph.langgraph_service import LangGraphService

llm_service = LLMService(settings=settings)

retriever = get_retriever(settings.RAG_DOCUMENT_PATH)


knowledge_service = KnowledgeService(retriever=retriever)
planner_agent = PlannerAgent(llm_service=llm_service)
research = ResearchAgent(llm_service=llm_service,knowledge_service=knowledge_service)
coding = CodingAgent(llm_service)
review = ReviewAgent(llm_service)
writer = WriterAgent(llm_service)



builder = LangGraphBuilder(planner=planner_agent,research=research,coding=coding,review=review,writer=writer)
graph_service = LangGraphService(builder=builder)



def get_llm_service():
    return llm_service

def get_graph_service():
    return graph_service