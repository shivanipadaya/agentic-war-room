# Configuration management using Pydantic Settings.
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """
    Application settings and environment variable validation schema.
    """
    # API Lifecycle
    GOOGLE_API_KEY: str
    TAVILY_API_KEY: str
    GEMINI_MODEL: str = "gemini-1.5-flash"
    
    # Infrastructure
    LOG_LEVEL: str = "INFO"
    MAX_RETRIES: int = 3
    REQUEST_TIMEOUT: int = 30
    
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

@lru_cache()
def get_settings() -> Settings:
    """
    Returns a cached instance of the application settings.
    
    Returns:
        Settings: The validated settings object.
    """
    return Settings()