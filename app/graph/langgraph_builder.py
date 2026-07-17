from app.agents.planner import PlannerAgent
from app.agents.coding import CodingAgent
from app.agents.review import ReviewAgent
from app.agents.writer import WriterAgent
from app.agents.research import ResearchAgent
from langgraph.graph import StateGraph, START, END
from app.graph.state import AgentState
from app.config.config import settings
from app.utils.logging import logger
from app.services.artifact_service import ArtifactService
from time import perf_counter
from datetime import datetime



PLANNER_NODE = "planner"
RESEARCH_NODE = "research"
CODING_NODE = "coding"
REVIEW_NODE = "review"
WRITER_NODE = "writer"
END_NODE = "end"
class LangGraphBuilder:

    def __init__(self,planner:PlannerAgent,research:ResearchAgent,coding:CodingAgent,review:ReviewAgent,writer:WriterAgent):
        self.artifact_service = ArtifactService()
        self.builder = StateGraph(AgentState)
        self.planner = planner
        self.research = research
        self.coding = coding
        self.review = review
        self.writer = writer
    
    async def planner_node(self,state:AgentState)->AgentState:
        logger.info("Planner started")
        start = perf_counter()
        state = await self.planner.run(state=state)
        logger.info(
            "Planner node history length = %d",
            len(state.execution_history),
        )
        elapsed = perf_counter() - start
        logger.info(
            "[%s] Planner completed in %.2fs",
            state.request_id,
            elapsed,
        )

        return state

    
    async def research_node(self,state:AgentState)->AgentState:
        logger.info("Research started")
        start = perf_counter()
        state = await self.research.run(state=state)
        elapsed = perf_counter() - start
        logger.info(
            "[%s] Research completed in %.2fs",
            state.request_id,
            elapsed,
        )

        return state
    
    async def coding_node(self,state:AgentState)->AgentState:
        
        is_retry = (
            state.review_result is not None
            and not state.review_result.passed
        )

        if is_retry:
            task = state.review_result.retry_task
        else:
            task = state.get_current_task()

        logger.info("Execution plan: %s",state.plan.model_dump())
        logger.info("Coding started")
        start = perf_counter()
        logger.info(
            "[%s] Coding (%d/%d): %s",
            state.request_id,
            state.current_step_index + 1,
            state.coding_step_count(),
            task,
        )
        state = await self.coding.run(
            state=state,
            task=task,
        )
        elapsed = perf_counter() - start
        logger.info(
            "Coding node history length = %d",
            len(state.execution_history),
        )
        logger.info(
            "[%s] Coding completed in %.2fs",
            state.request_id,
            elapsed,
        )
        if not is_retry:
            state.current_step_index += 1

        return state
    
    async def review_node(self,state:AgentState)->AgentState:
        logger.info("Review started")
        start = perf_counter()
        state = await self.review.run(state=state)

        elapsed = perf_counter() - start
        logger.info(
            "[%s] Review completed in %.2fs",
            state.request_id,
            elapsed,
        )
        logger.info(
            "Review node history length = %d",
            len(state.execution_history),
        )
        logger.info(
        "Review completed. Passed=%s Confidence=%.2f",
            state.review_result.passed,
            state.review_result.confidence,
        )

        return state
    
    async def writer_node(self,state:AgentState)->AgentState:
        logger.info("Writer started")
        start = perf_counter()
        state = await self.writer.run(state=state)
        elapsed = perf_counter() - start
        total_time = (
             datetime.now() - state.workflow_started_at
        ).total_seconds()

        logger.info(
            "Writer node history length = %d",
            len(state.execution_history),
        )
        logger.info(
            "[%s] Writer completed in %.2fs",
            state.request_id,
            elapsed,
            
        )
        logger.info(
            "[%s] Workflow completed in %.2fs",
            state.request_id,
            total_time,
        )

        logger.info(
            "[%s] Total artifacts: %d",
            state.request_id,
            len(state.generated_artifacts),
        )
        logger.info(state.final_response.summary)
        logger.info("Writer ended")
        try:
            self.artifact_service.save(state.generated_artifacts)
            logger.info("Artifacts saved successfully.")
        except Exception:
            logger.exception("Failed to save artifacts.")
        return state
    
    def route_after_planner(self,state:AgentState)->str:

        if state.plan.needs_research :
            logger.info("Routing: Planner -> Research")
            return RESEARCH_NODE
        
        logger.info("Routing: Planner -> Coding")
        return CODING_NODE
    
    def route_after_review(self,state:AgentState)->str:
        
        if state.review_result.passed:
            return WRITER_NODE
        
        state.retry_attempts += 1
        if state.retry_attempts >= settings.MAX_RETRIES:
            logger.warning("Retry %d/%d failed",state.retry_attempts,settings.MAX_RETRIES)
            return WRITER_NODE
        
        logger.info("Routing: Review -> Coding (Retry)")
        return CODING_NODE
    
    def route_after_coding(self,state: AgentState) -> str:

        if state.is_retry():
            logger.info("Routing: Coding -> Review")
            return REVIEW_NODE

        if (
            state.current_step_index
            < state.coding_step_count()
        ):
            return CODING_NODE

        return REVIEW_NODE
    
    def build(self):

        self.builder.add_node(
            PLANNER_NODE,
            self.planner_node,
        )
        self.builder.add_node(
            RESEARCH_NODE,
            self.research_node
        )
        self.builder.add_node(
            CODING_NODE,
            self.coding_node
        )
        self.builder.add_node(
            REVIEW_NODE,
            self.review_node
        )
        self.builder.add_node(
            WRITER_NODE,
            self.writer_node
        )

        self.builder.add_edge(
            START,
            PLANNER_NODE,
        )

        self.builder.add_conditional_edges(
            PLANNER_NODE,
            self.route_after_planner,
            {
                RESEARCH_NODE:RESEARCH_NODE,
                CODING_NODE:CODING_NODE
            }
        )
        self.builder.add_edge(
            RESEARCH_NODE,
            CODING_NODE
        )
        self.builder.add_conditional_edges(
            CODING_NODE,
            self.route_after_coding,
            {
                CODING_NODE: CODING_NODE,
                REVIEW_NODE: REVIEW_NODE,
            },
        )
        self.builder.add_conditional_edges(
            REVIEW_NODE,
            self.route_after_review,
            {
                CODING_NODE:CODING_NODE,
                WRITER_NODE:WRITER_NODE
            }
        )
        self.builder.add_edge(
            WRITER_NODE,
            END
        )
        return self.builder.compile()



