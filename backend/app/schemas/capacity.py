"""Pydantic schemas for the Capacity Engine."""

from pydantic import BaseModel, Field


# ── Request ──

class CapacityInput(BaseModel):
    """Input parameters for capacity calculation."""

    total_users: int = Field(..., gt=0, description="Total registered users")
    dau: int = Field(..., gt=0, description="Daily Active Users")
    requests_per_user_per_day: int = Field(default=50, gt=0, description="Average API requests per user per day")
    read_write_ratio: float = Field(default=10.0, gt=0, description="Reads per write (e.g., 10 = 10:1)")
    avg_request_payload_kb: float = Field(default=5.0, gt=0, description="Average request payload in KB")
    avg_object_size_mb: float = Field(default=1.0, gt=0, description="Average stored object size in MB")
    peak_multiplier: float = Field(default=5.0, gt=1.0, description="Peak traffic multiplier over average")
    data_retention_years: int = Field(default=5, gt=0, description="How many years to retain data")


# ── Response ──

class CapacityFormula(BaseModel):
    """A single capacity formula with its calculation."""

    name: str
    formula: str
    result: str


class InfraRecommendations(BaseModel):
    """Infrastructure sizing recommendations based on capacity math."""

    api_instances_min: int
    api_instances_max: int
    database_type: str                    # "single", "replicated", "sharded"
    database_replicas: int
    cache_needed: bool
    cache_size_gb: float
    queue_needed: bool
    cdn_needed: bool


class CapacityOutput(BaseModel):
    """Complete capacity calculation output."""

    # Traffic
    total_requests_per_day: int
    average_rps: float
    peak_rps: float
    read_rps: float
    write_rps: float

    # Storage
    daily_data_ingestion_gb: float
    monthly_storage_gb: float
    yearly_storage_tb: float
    total_storage_tb: float           # Over retention period

    # Bandwidth
    incoming_bandwidth_mbps: float
    outgoing_bandwidth_mbps: float

    # Cache
    cache_size_gb: float

    # Recommendations
    recommendations: InfraRecommendations

    # Show the math
    formulas: list[CapacityFormula]
