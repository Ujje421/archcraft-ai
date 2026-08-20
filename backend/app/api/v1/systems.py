"""Systems API — CRUD operations for system designs."""

from fastapi import APIRouter

router = APIRouter(prefix="/systems", tags=["Systems"])


@router.get(
    "",
    summary="List all systems",
    description="Returns a list of all saved system designs.",
)
async def list_systems() -> dict:
    """List systems — placeholder until database is connected."""
    return {"items": [], "total": 0, "page": 1, "pages": 0}


@router.post(
    "",
    summary="Create a new system",
    description="Manually create a new system design (without AI generation).",
    status_code=201,
)
async def create_system() -> dict:
    """Create system — placeholder until database is connected."""
    return {"message": "System CRUD will be implemented after database setup"}


@router.post(
    "/generate",
    summary="AI-generate a system design",
    description="Generate a complete system design from a natural language prompt using the AI engine.",
    status_code=201,
)
async def generate_system() -> dict:
    """Generate system — placeholder until AI engine is implemented."""
    return {"message": "AI generation will be implemented in Sprint 3-4"}
