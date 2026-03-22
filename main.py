# Entry point for the Strategic Signal agentic war room.
import uuid
from langgraph.graph import StateGraph, END
from pydantic import ValidationError

# Import our components
from src.agents.state import AgentState
from src.agents.nodes.scout import scout_node
from src.agents.nodes.strategist import strategist_node
from src.core.config import get_settings
from src.core.logger import setup_logger

# pydantic_settings handles .env loading. load_dotenv() is redundant.
logger = setup_logger(__name__)

def build_graph():
    """
    Constructs the LangGraph state machine for the agentic workflow.
    
    Returns:
        CompiledGraph: The executable graph.
    """
    # Initialize the Graph
    workflow = StateGraph(AgentState)

    # Add Nodes
    workflow.add_node("scout", scout_node)
    workflow.add_node("strategist", strategist_node)

    # Define Edges
    workflow.set_entry_point("scout")
    workflow.add_edge("scout", "strategist")
    workflow.add_edge("strategist", END)

    # Compile
    return workflow.compile()

if __name__ == "__main__":
    try:
        # This call validates all environment variables on startup.
        # If it fails, the app will panic as per the spec.
        settings = get_settings()
        logger.info("Configuration loaded successfully.", extra={"model": settings.GEMINI_MODEL})
    except ValidationError as e:
        logger.error(f"CRITICAL: Configuration validation failed. Missing or invalid environment variables.\n{e}")
        exit(1) # Panic as per spec

    app = build_graph()
    
    topic = "Apple Intelligence vs Google Gemini features"
    trace_id = str(uuid.uuid4())
    logger.info(f"Starting War Room Session for: {topic}", extra={"trace_id": trace_id})
    
    initial_state = {
        "query": topic,
        "trace_id": trace_id,
        "error": None,
        "metadata": {}
    }
    result = app.invoke(initial_state)
    
    if result.get("error"):
        logger.error(f"Agent run failed: {result['error']}", extra={"trace_id": trace_id})
    else:
        final_report = result.get("strategic_analysis", "No analysis was generated.")
        logger.info("="*30, extra={"trace_id": trace_id})
        logger.info("FINAL STRATEGIC REPORT", extra={"trace_id": trace_id})
        logger.info("="*30, extra={"trace_id": trace_id})
        logger.info(f"\n{final_report}", extra={"trace_id": trace_id})