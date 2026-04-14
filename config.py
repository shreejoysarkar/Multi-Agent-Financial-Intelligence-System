"""Application configuration using pydantic-settings."""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # gemini Configuration
    GEMINI_API_KEY: str

    # Qdrant Cloud Configuration
    qdrant_url: str
    qdrant_api_key: str

    # Model Configuration
    embedding_model: str = "gemini-embedding-001"
    llm_model: str = "gemini-2.5-flash"
    llm_temperature: float = 0.0

    # Logging
    log_level: str = "INFO"

    # API Settings
    api_host: str = "0.0.0.0"
    api_port: int = 8000

    # Application Info
    app_name: str = "RAG Q&A System"
    app_version: str = "0.1.0"


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()