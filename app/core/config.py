from __future__ import annotations

import os
from functools import lru_cache
from typing import Optional


class Settings:
    """Minimal settings — no external settings lib required for on-ramp."""

    def __init__(self) -> None:
        self.database_url: str = os.environ.get(
            "DATABASE_URL", "sqlite+aiosqlite:////tmp/aflo.db"
        )
        self.app_env: str = os.environ.get("APP_ENV", "development")
        self.log_level: str = os.environ.get("LOG_LEVEL", "INFO")
        self.openai_api_key: Optional[str] = os.environ.get("OPENAI_API_KEY")
        self.openai_base_url: str = os.environ.get(
            "OPENAI_BASE_URL", "https://api.openai.com/v1"
        )
        self.openai_model: str = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")
        self.min_auto_validate_confidence: float = float(
            os.environ.get("MIN_AUTO_VALIDATE_CONFIDENCE", "0.92")
        )
        self.material_change_pct_threshold: float = float(
            os.environ.get("MATERIAL_CHANGE_PCT_THRESHOLD", "0.05")
        )


@lru_cache
def get_settings() -> Settings:
    return Settings()
