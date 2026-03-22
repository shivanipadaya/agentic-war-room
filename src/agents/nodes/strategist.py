# Strategist node for synthesizing intelligence and generating business counter-moves.
from src.agents.state import AgentState
from src.core.logger import setup_logger
from src.core.config import get_settings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from src.agents.prompts import STRATEGIST_PROMPT

logger = setup_logger(__name__)

def strategist_node(state: AgentState) -> AgentState:
    """
    Analyzes raw intelligence and generates strategic recommendations using LLM.
    
    Args:
        state (AgentState): The current agent state containing raw_data.
        
    Returns:
        AgentState: The updated state with strategic_analysis.
    """
    trace_id = state.get("trace_id")
    logger.info("--- [STRATEGIST] Synthesizing Intelligence ---", extra={"trace_id": trace_id})

    if state.get("error"):
        logger.warning(f"Skipping strategist due to previous error: {state['error']}", extra={"trace_id": trace_id})
        return state

    settings = get_settings()

    llm = ChatGoogleGenerativeAI(model=settings.GEMINI_MODEL, google_api_key=settings.GOOGLE_API_KEY)
    
    prompt = ChatPromptTemplate.from_template(STRATEGIST_PROMPT)
    
    chain = prompt | llm
    response = chain.invoke({"query": state["query"], "raw_data": state["raw_data"]})
    
    state["strategic_analysis"] = response.content
    return state