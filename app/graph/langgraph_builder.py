from app.agents.planner import PlannerAgent
from app.agents.coding import CodingAgent
from app.agents.review import ReviewAgent
from app.agents.writer import WriterAgent
from app.agents.research import ResearchAgent
from langgraph.graph import StateGraph, START, END
from app.graph.state import AgentState,AgentType
from app.config.config import settings
from app.utils.logging import logger

PLANNER_NODE = "planner"
RESEARCH_NODE = "research"
CODING_NODE = "coding"
REVIEW_NODE = "review"
WRITER_NODE = "writer"
END_NODE = "end"
class LangGraphBuilder:

    def __init__(self,planner:PlannerAgent,research:ResearchAgent,coding:CodingAgent,review:ReviewAgent,writer:WriterAgent):
        self.builder = StateGraph(AgentState)
        self.planner = planner
        self.research = research
        self.coding = coding
        self.review = review
        self.writer = writer
    
    async def planner_node(self,state:AgentState)->AgentState:
        logger.info("Planner started")
        state = await self.planner.run(state=state)
        logger.info("Planner ended")

        return state

    
    async def research_node(self,state:AgentState)->AgentState:
        logger.info("Research started")
        state = await self.research.run(state=state)
        logger.info("Research ended")

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

        print(state.plan.model_dump())
        logger.info("Coding started")
        logger.info(
            "Coding task (%s/%s): %s",
            state.current_step_index + 1,
            state.coding_step_count(),
            task,
        )
        state = await self.coding.run(
            state=state,
            task=task,
        )
        logger.info("Coding ended")
        if not is_retry:
            state.current_step_index += 1

        return state
    
    async def review_node(self,state:AgentState)->AgentState:
        logger.info("Review started")
        state = await self.review.run(state=state)
        logger.info("Review ended")
        logger.info(
        "Review completed. Passed=%s Confidence=%.2f",
            state.review_result.passed,
            state.review_result.confidence,
        )

        return state
    
    async def writer_node(self,state:AgentState)->AgentState:
        logger.info("Writer started")
        state = await self.writer.run(state=state)
        logger.info("Writer ended")
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
            return WRITER_NODE
        
        logger.info("Routing: Review -> Coding (Retry)")
        return CODING_NODE
    
    def route_after_coding(self,state: AgentState) -> str:

        if (
        state.review_result
        and not state.review_result.passed
        ):
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



