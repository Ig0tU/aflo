from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    database_url: str = "sqlite+aiosqlite:///./aflo.db"
    app_env: str = "development"
    log_level: str = "INFO"
    openai_api_key: str | None = None
    openai_base_url: str = "https://api.openai.com/v1"
    openai_model: str = "gpt-4o-mini"

    # Deterministic validation thresholds
    min_auto_validate_confidence: float = 0.92
    material_change_pct_threshold: float = 0.05  # 5%


@lru_cache
def get_settings() -> Settings:
    return Settings()
