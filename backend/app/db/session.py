"""Async SQLAlchemy engine and session factory."""

from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings

# ── Engine ──
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    pool_size=20,
    max_overflow=10,
    pool_pre_ping=True,
)

# ── Session factory ──
async_session_factory = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


# ── Base model for all ORM classes ──
class Base(DeclarativeBase):
    """Declarative base for all SQLAlchemy models."""

    pass


# ── Dependency for FastAPI routes ──
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Yield an async database session, auto-closing on completion."""
    async with async_session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
