# Copilot Instructions for Agentic War Room

These notes are written for AI coding agents to be productive immediately.
They assume familiarity with LangGraph-style agent pipelines and Python 3.11+.

---
## 1. Big Picture Architecture

- **Entry point**: `main.py` (CLI/API). It composes a graph from `src/agents/graph.py` and executes it.
- **Three logical nodes** live under `src/agents/nodes/`:
  - `scout.py` – deep research scrapers (Firecrawl/Tavily clients). Pulls raw data.
  - `strategist.py` – reasoning engine that consumes deltas and produces strategy.
  - _(Archivist state handling is partly in `src/agents/state.py`)_
- **State** is defined in `src/agents/state.py` with TypedDict/Pydantic and is the _only_ mutable data.
  All nodes receive and return `AgentState` objects; idempotency is mandatory.

- **Core utilities** reside in `src/core/`:
  - `config.py` – single source of truth for env vars via `pydantic_settings`.
  - `logger.py` – context‑aware JSON/structured logging; must be used instead of `print()`.
  - `exceptions.py` – domain-specific errors; inference code should catch them.

- **Services** and **tools** are abstractions for external APIs (LLM clients, Tavily, etc.)
  under `src/services/` and `src/tools/`. Treat them as black boxes when extending.


## 2. Developer Workflows

- **Setup**:
  1. Copy `.env.template` to `.env` and fill in keys (GOOGLE_API_KEY, etc.).
  2. `pip install -r requirements.txt` (virtualenv/venv recommended).

- **Run the system**:
  ```sh
  python main.py --query "some market intelligence topic"
  ```
  `main.py` automatically loads settings via `get_settings()`; it will crash on missing vars.

- **Logging & debugging**: run with `LOG_LEVEL=DEBUG` to see node‑level traces. Outputs are
  line‑oriented JSON for ingestion by ELK/GCP.

- **Tests**: none currently in the repo, but follow naming conventions under `tests/`
  (unit files mirror `src/` structure).  Use `pytest` when they exist.


## 3. Project Conventions

- **No global state**: All state flows through `AgentState`. Do not import or mutate a
  module‑level variable. If you need a cache, put it behind `functools.lru_cache`.

- **Configuration**: Use `get_settings()` from `src/core/config.py` everywhere. Treat
  settings as immutable after startup.

- **Error handling**: Wrap every external call (LLM, HTTP) in a try/except catching
  `src.core.exceptions.BaseError` and log then raise or return a failure state.

- **LLM hygiene**:
  - Always specify `temperature` and `timeout`.
  - Add a `retry_policy` (use exponential backoff helpers if available).
  - Log token counts when returned by SDKs for cost analysis.

- **Logging**: never use `print()`. Acquire a logger with `from src.core.logger import setup_logger`
  and call `setup_logger(__name__)` at module top. Include a `trace_id` field in every log.

- **Prompt standards**: See the bottom of `AGENT.md` for an example prompt string. Any
  generated prompt should preamble with:
  > "You are a Google Staff Software Engineer..." and restate the discipline above.


## 4. Patterns and Examples

- **Defining a node** (`src/agents/nodes/strategist.py`):
  ```python
  from src.agents.state import AgentState
  def run(state: AgentState) -> AgentState:
      # do reasoning, call LLM service
      state['strategic_analysis'] = analysis
      return state
  ```
  Keep logic pure; configuration comes from `get_settings()` inside the node.

- **Graph structure** (`src/agents/graph.py`): look for a function that returns a
  LangGraph `Graph` object building the three nodes above with dependencies.

- **State schema**: `AgentState` uses `Annotated[list, add_messages]` to mark a list of
  messages for LangGraph; always import `add_messages` when defining new keys.


## 5. External Dependencies & Integration Points

- **Firecrawl / Tavily** – wrappers under `src/tools/*`; used by the Scout node for crawling.
  They expect API keys from environment variables documented in `.env.template`.

- **Gemini / OpenAI** – LLM clients in `src/services/`; selection dictated by
  `get_settings().GEMINI_MODEL` etc. The Strategist node is the main consumer.

- **LangGraph** – graph execution engine; nodes must follow its message passing
  conventions. The repository is built around its checkpointing features;
  state is persisted between runs.


## 6. Writing or Extending Code

1. **Start with state/schema**: add new fields to `AgentState` in `src/agents/state.py`
   with appropriate type and annotations.
2. **Build a node** in `src/agents/nodes/` with a `run(state)` function.
3. **Register it** in `src/agents/graph.py` with proper dependencies (e.g. scout -> archivist -> strategist).
4. **Add config** in `src/core/config.py` and update `.env.template`.
5. **Log extensively** using `setup_logger` and include `trace_id` from state.


---

This document should be kept short (20–50 lines); rely on `AGENT.md` and `README.md` for
deeper context. Feel free to ask for clarification if you hit an unfamiliar pattern.

> _Ask the maintainer for feedback or missing details; update this file accordingly._
