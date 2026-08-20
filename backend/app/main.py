"""ArchCraft Backend — FastAPI application entry point."""

from contextlib import asynccontextmanager
from collections.abc import AsyncIterator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.v1 import capacity, components, systems


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Application startup and shutdown events."""
    # Startup
    print(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}...")
    print(f"   Environment: {settings.APP_ENV}")
    print(f"   Database: {settings.DATABASE_URL.split('@')[-1] if '@' in settings.DATABASE_URL else 'not configured'}")
    yield
    # Shutdown
    print(f"Shutting down {settings.APP_NAME}...")


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description=(
        "AI-native system design engineering platform. "
        "Design, understand, evaluate, and evolve software architectures."
    ),
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# ── CORS ──
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Health check ──
@app.get("/health", tags=["Health"])
async def health_check() -> dict:
    """Health check endpoint."""
    return {
        "status": "healthy",
        "version": settings.APP_VERSION,
        "app": settings.APP_NAME,
    }


# ── API v1 routes ──
app.include_router(capacity.router, prefix="/api/v1")
app.include_router(components.router, prefix="/api/v1")
app.include_router(systems.router, prefix="/api/v1")
