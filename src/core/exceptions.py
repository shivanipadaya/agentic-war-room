# Domain-specific exception hierarchy.
class AgentError(Exception):
    """Base exception for agent errors."""
    pass

class ConfigurationError(AgentError):
    """Raised when configuration is missing or invalid."""
    pass