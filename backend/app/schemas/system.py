"""Pydantic schemas for System CRUD and architecture graph operations."""

import uuid
from datetime import datetime

from pydantic import BaseModel, Field


# ── Graph primitives ──

class Position(BaseModel):
    """Canvas position for a node."""

    x: float = 0.0
    y: float = 0.0


class NodeSchema(BaseModel):
    """A node in the architecture graph."""

    node_id: str = Field(..., description="Logical ID (e.g., 'redis_cache')")
    type: str = Field(..., description="Component type: database, cache, service, etc.")
    technology: str | None = Field(None, description="Specific tech: PostgreSQL, Redis, etc.")
    label: str = Field(..., description="Display label")
    min_level: int = Field(default=0, ge=0, le=4)
    position: Position = Field(default_factory=Position)
    metadata: dict = Field(default_factory=dict)


class ConnectionSchema(BaseModel):
    """An edge connecting two nodes."""

    source_node_id: str
    target_node_id: str
    label: str | None = None
    protocol: str | None = None      # HTTPS, gRPC, async, TCP
    min_level: int = Field(default=0, ge=0, le=4)
    metadata: dict = Field(default_factory=dict)


class ArchitectureGraph(BaseModel):
    """The complete architecture graph for a system."""

    nodes: list[NodeSchema] = Field(default_factory=list)
    connections: list[ConnectionSchema] = Field(default_factory=list)


# ── System CRUD ──

class SystemCreate(BaseModel):
    """Create a new system design (manual, not AI-generated)."""

    title: str = Field(..., min_length=1, max_length=255)
    description: str | None = None
    domain: str | None = None
    active_level: int = Field(default=2, ge=0, le=4)
    architecture_style: str = Field(default="microservices")
    parameters: dict = Field(default_factory=dict)


class SystemGenerateRequest(BaseModel):
    """Request to AI-generate a full system design."""

    prompt: str = Field(..., min_length=5, description="e.g., 'Design a food delivery platform'")
    parameters: dict = Field(default_factory=dict)
    level: int = Field(default=2, ge=0, le=4)
    architecture_style: str = Field(default="auto")  # monolith, microservices, auto


class SystemUpdate(BaseModel):
    """Partial update to a system."""

    title: str | None = None
    description: str | None = None
    active_level: int | None = Field(None, ge=0, le=4)
    parameters: dict | None = None


class SystemResponse(BaseModel):
    """Full system response returned from the API."""

    id: uuid.UUID
    title: str
    description: str | None
    domain: str | None
    prompt: str | None
    active_level: int
    architecture_style: str
    parameters: dict
    architecture: ArchitectureGraph
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class SystemListItem(BaseModel):
    """Lightweight system for list views."""

    id: uuid.UUID
    title: str
    domain: str | None
    active_level: int
    node_count: int = 0
    created_at: datetime

    model_config = {"from_attributes": True}


class PaginatedSystems(BaseModel):
    """Paginated response for system list."""

    items: list[SystemListItem]
    total: int
    page: int
    pages: int


# ── Graph Diff (AI modifications) ──

class GraphDiff(BaseModel):
    """A diff describing changes the AI wants to make to the graph."""

    add_nodes: list[NodeSchema] = Field(default_factory=list)
    remove_nodes: list[str] = Field(default_factory=list)         # node_ids to remove
    add_connections: list[ConnectionSchema] = Field(default_factory=list)
    remove_connections: list[str] = Field(default_factory=list)   # connection descriptions
    explanation: str = ""
    warnings: list[str] = Field(default_factory=list)


# ── API response wrapper ──

class APIResponse(BaseModel):
    """Standard API response envelope."""

    success: bool = True
    data: dict | list | None = None
    error: dict | None = None
