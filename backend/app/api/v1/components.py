"""Component Knowledge Base API — browse and query infrastructure components."""

from fastapi import APIRouter, HTTPException, Query

from app.knowledge.components_data import COMPONENTS_DB

router = APIRouter(prefix="/components", tags=["Component Knowledge Base"])


@router.get(
    "",
    summary="List all components",
    description="Returns all infrastructure components in the knowledge base, optionally filtered by category.",
)
async def list_components(
    category: str | None = Query(None, description="Filter by category: database, cache, queue, etc."),
) -> list[dict]:
    """Return all components, optionally filtered by category."""
    components = list(COMPONENTS_DB.values())
    if category:
        components = [c for c in components if c.get("category") == category]
    return components


@router.get(
    "/{slug}",
    summary="Get component details",
    description="Returns full deep-dive information for a specific infrastructure component.",
)
async def get_component(slug: str) -> dict:
    """Return detailed knowledge for a single component."""
    component = COMPONENTS_DB.get(slug)
    if not component:
        raise HTTPException(status_code=404, detail=f"Component '{slug}' not found")
    return component


@router.get(
    "/categories/list",
    summary="List component categories",
    description="Returns all available component categories (database, cache, queue, etc.).",
)
async def list_categories() -> list[str]:
    """Return all unique component categories."""
    categories = sorted({c.get("category", "unknown") for c in COMPONENTS_DB.values()})
    return categories
