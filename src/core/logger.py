# Structured logging utility for the agentic war room.
import logging
import sys
from src.core.config import get_settings

def setup_logger(name: str):
    """
    Configures and returns a structured logger with standard formatting.
    
    Args:
        name (str): The name of the logger, typically __name__.
        
    Returns:
        logging.Logger: A configured logger instance.
    """
    logger = logging.getLogger(name)
    
    try:
        settings = get_settings()
        logger.setLevel(settings.LOG_LEVEL)
    except Exception:
        logger.setLevel(logging.INFO)
    
    # Standard format for cloud logging parsing
    formatter = logging.Formatter(
        '%(asctime)s | %(levelname)s | [%(name)s] | %(message)s'
    )
    
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)
    
    if not logger.handlers:
        logger.addHandler(handler)
    return logger