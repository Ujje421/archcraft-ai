"""Capacity Engine API — deterministic capacity calculation endpoint."""

from fastapi import APIRouter

from app.engines.capacity_engine import calculate_capacity
from app.schemas.capacity import CapacityInput, CapacityOutput

router = APIRouter(prefix="/capacity", tags=["Capacity Engine"])


@router.post(
    "/calculate",
    response_model=CapacityOutput,
    summary="Calculate system capacity",
    description="Compute traffic, storage, bandwidth, cache sizing, and infrastructure "
    "recommendations from input parameters. All calculations are deterministic — no AI involved.",
)
async def calculate(input_data: CapacityInput) -> CapacityOutput:
    """Calculate capacity metrics from system parameters.

    This is a pure computation endpoint — no database or AI calls.
    Every formula is shown in the response so users can verify the math.
    """
    return calculate_capacity(input_data)
