# State definitions for the LangGraph agent workflow.
from typing import TypedDict, Optional, Dict

class AgentState(TypedDict):
    """
    Represents the shared state passed between nodes in the LangGraph.
    """
    query: str
    raw_data: str
    strategic_analysis: str
    # Production-grade fields for tracing and error handling
    trace_id: str
    error: Optional[str]
    metadata: Dict