"""ArchCraft backend configuration — loaded from environment variables."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from .env or environment variables."""

    # ── App ──
    APP_NAME: str = "ArchCraft"
    APP_VERSION: str = "0.1.0"
    APP_ENV: str = "development"  # development | staging | production
    APP_SECRET_KEY: str = "change-me-in-production"
    DEBUG: bool = True

    # ── Database ──
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/archcraft"

    # ── Redis ──
    REDIS_URL: str = "redis://localhost:6379/0"

    # ── AI Providers ──
    OPENAI_API_KEY: str = ""
    GEMINI_API_KEY: str = ""
    DEFAULT_LLM_PROVIDER: str = "openai"  # openai | gemini

    # ── CORS ──
    CORS_ORIGINS: list[str] = ["http://localhost:3000", "http://localhost:5173"]

    # ── Rate Limiting ──
    RATE_LIMIT_ENABLED: bool = True
    RATE_LIMIT_GENERATE: int = 10   # per hour
    RATE_LIMIT_AI: int = 60         # per hour

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": True,
    }


settings = Settings()
