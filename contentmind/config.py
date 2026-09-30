from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""

    app_name: str = "ContentMind"
    app_env: str = "development"
    database_url: str = "sqlite:///./contentmind.db"
    anthropic_api_key: str | None = None
    openai_api_key: str | None = None
    cognee_api_key: str | None = None

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


@lru_cache
def get_settings() -> Settings:
    return Settings()
