AGENT.md: High-Performance Agent Architecture (L6/L7 Spec)
1. The Golden Rules (Standard Operating Procedures)
Zero Global State: All nodes must be idempotent. The AgentState is the only source of truth.

Structured Telemetry: print() is a bug. Use structured logging (JSON preferred for ELK/GCP) with unique trace_id for every run.

The Config Contract: Use Pydantic for configuration. If a required environment variable is missing or malformed, the system must Panic (crash on startup) to prevent silent failures in mid-workflow.

Fail-Safe Inference: All LLM calls must have a defined timeout and a retry_policy (Exponential Backoff).

Mandatory Documentation: Every file must have a top-level purpose comment, and every function/class must have a docstring.


2. System Topology
We follow a strictly decoupled folder structure to ensure 100% test coverage availability.

Plaintext
/
├── .env.template           # Clear documentation of required secrets
├── main.py                 # The entry point (CLI/API)
├── src/
│   ├── agents/
│   │   ├── graph.py        # The DAG (Directed Acyclic Graph) definition
│   │   ├── state.py        # Pydantic/TypedDict state schemas
│   │   └── nodes/          # Atomic logic units (Logic-only, no config hardcoding)
│   ├── core/
│   │   ├── config.py       # Pydantic Settings (The "Source of Truth")
│   │   ├── logger.py       # Custom Logger (Interceptors/Handlers)
│   │   └── exceptions.py   # Domain-specific error hierarchy
│   ├── services/           # LLM Clients (Abstractions over Gemini/OpenAI)
│   └── tools/              # Registry for Tavily, Search, etc.
└── tests/                  # Integration & Unit tests

3. Engineering Implementation Standards
A. The Schema-First Approach
Never pass raw strings. Use src/agents/state.py to define the shape of your data.

Python
from typing import Annotated, TypedDict
from langgraph.graph.message import add_messages

class AgentState(TypedDict):
    query: str
    context: Annotated[list, add_messages]
    strategic_analysis: str
    metadata: dict  # Used for tracing/cost tracking
B. The Config Validator (src/core/config.py)
At Google, we use lru_cache to ensure the config is only parsed once and remains immutable.

Python
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    # API Lifecycle
    GOOGLE_API_KEY: str
    GEMINI_MODEL: str = "gemini-2.5-flash"
    
    # Infrastructure
    LOG_LEVEL: str = "INFO"
    MAX_RETRIES: int = 3
    REQUEST_TIMEOUT: int = 30
    
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

@lru_cache()
def get_settings() -> Settings:
    return Settings()
C. Observability & Logging (src/core/logger.py)
Implementation of a "Context-Aware" logger that allows us to track an agent's thought process across multiple nodes.

Python
import logging
import sys

def setup_logger(name: str):
    logger = logging.getLogger(name)
    logger.setLevel(get_settings().LOG_LEVEL)
    
    # Standard format for cloud logging parsing
    formatter = logging.Formatter(
        '%(asctime)s | %(levelname)s | [%(name)s] | %(message)s'
    )
    
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)
    
    if not logger.handlers:
        logger.addHandler(handler)
    return logger

D. Documentation Standards
Every file must start with a top-level comment describing its purpose.
Every function and class must have a Google-style docstring.

4. Inference Hygiene
When calling Gemini (or any LLM):

Always specify a temperature.

Always wrap in a try-except block targeting src.core.exceptions.

Log the Token Count (if the SDK provides it) for cost-visibility.

5. Instructions for Gemini (The Prompt)
"You are a Google Staff Software Engineer. Every line of code you generate must follow the AGENT.md spec. Prioritize type safety, avoid print() in favor of the src.core.logger, and use the validated get_settings() for all parameters. If a request would violate these production standards, explain why and provide the correct architectural alternative."