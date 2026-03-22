# Scout node for deep market research using external search tools.
from src.agents.state import AgentState
from src.core.logger import setup_logger
from src.core.config import get_settings
from src.core.exceptions import AgentError
from langchain_community.tools.tavily_search import TavilySearchResults

logger = setup_logger(__name__)

def scout_node(state: AgentState) -> AgentState:
    """
    Performs deep research on the provided query using Tavily.
    
    Args:
        state (AgentState): The current agent state containing the query.
        
    Returns:
        AgentState: The updated state with raw_data or an error message.
    """
    trace_id = state.get("trace_id")
    logger.info(f"--- [SCOUT] Initiating Deep Research on: {state['query']} ---", extra={"trace_id": trace_id})

    try:
        # TavilySearchResults will automatically pick up TAVILY_API_KEY from env
        # which is validated by get_settings() on startup
        tool = TavilySearchResults(max_results=3)
        results = tool.invoke(state['query'])
        context = "\n".join([f"Source: {r['url']}\nContent: {r['content']}" for r in results])
        
        state['raw_data'] = context
        state['error'] = None
        return state
    except Exception as e:
        logger.error(f"Scout node failed during research: {str(e)}", extra={"trace_id": trace_id})
        state['error'] = f"Scout node failed: {str(e)}"
        return state