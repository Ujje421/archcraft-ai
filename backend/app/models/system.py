"""System and architecture graph ORM models."""

import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


class System(Base):
    """A system design project — the top-level entity."""

    __tablename__ = "systems"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    domain: Mapped[str] = mapped_column(String(100), nullable=True)
    prompt: Mapped[str] = mapped_column(Text, nullable=True)
    active_level: Mapped[int] = mapped_column(Integer, default=2)
    architecture_style: Mapped[str] = mapped_column(String(50), default="microservices")
    parameters: Mapped[dict] = mapped_column(JSONB, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # Relationships
    nodes: Mapped[list["ArchNode"]] = relationship(back_populates="system", cascade="all, delete-orphan")
    connections: Mapped[list["ArchConnection"]] = relationship(
        back_populates="system", cascade="all, delete-orphan"
    )
    sections: Mapped[list["DesignSection"]] = relationship(
        back_populates="system", cascade="all, delete-orphan"
    )
    decisions: Mapped[list["Decision"]] = relationship(
        back_populates="system", cascade="all, delete-orphan"
    )
    versions: Mapped[list["SystemVersion"]] = relationship(
        back_populates="system", cascade="all, delete-orphan"
    )


class ArchNode(Base):
    """A node in the architecture graph (e.g., PostgreSQL, Redis, API Gateway)."""

    __tablename__ = "arch_nodes"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    system_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("systems.id", ondelete="CASCADE"), nullable=False
    )
    node_id: Mapped[str] = mapped_column(String(100), nullable=False)  # Logical ID (e.g., "redis_cache")
    type: Mapped[str] = mapped_column(String(50), nullable=False)       # "database", "cache", "service", etc.
    technology: Mapped[str] = mapped_column(String(100), nullable=True)  # "PostgreSQL", "Redis", etc.
    label: Mapped[str] = mapped_column(String(255), nullable=False)
    min_level: Mapped[int] = mapped_column(Integer, default=0)
    position_x: Mapped[float] = mapped_column(default=0.0)
    position_y: Mapped[float] = mapped_column(default=0.0)
    metadata_: Mapped[dict] = mapped_column("metadata", JSONB, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    system: Mapped["System"] = relationship(back_populates="nodes")
    component: Mapped["Component | None"] = relationship(
        "Component",
        primaryjoin="foreign(ArchNode.technology) == Component.slug",
        viewonly=True,
        uselist=False,
    )


class ArchConnection(Base):
    """An edge in the architecture graph connecting two nodes."""

    __tablename__ = "arch_connections"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    system_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("systems.id", ondelete="CASCADE"), nullable=False
    )
    source_node_id: Mapped[str] = mapped_column(String(100), nullable=False)
    target_node_id: Mapped[str] = mapped_column(String(100), nullable=False)
    label: Mapped[str] = mapped_column(String(255), nullable=True)
    protocol: Mapped[str] = mapped_column(String(50), nullable=True)  # "HTTPS", "gRPC", "async", "TCP"
    min_level: Mapped[int] = mapped_column(Integer, default=0)
    metadata_: Mapped[dict] = mapped_column("metadata", JSONB, default=dict)

    # Relationships
    system: Mapped["System"] = relationship(back_populates="connections")


class DesignSection(Base):
    """One of the 26 schema sections for a system design."""

    __tablename__ = "design_sections"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    system_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("systems.id", ondelete="CASCADE"), nullable=False
    )
    section_key: Mapped[str] = mapped_column(String(100), nullable=False)  # e.g., "problem_definition"
    section_order: Mapped[int] = mapped_column(Integer, nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    content: Mapped[dict] = mapped_column(JSONB, default=dict)

    # Relationships
    system: Mapped["System"] = relationship(back_populates="sections")


class Decision(Base):
    """An architectural decision record (ADR)."""

    __tablename__ = "decisions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    system_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("systems.id", ondelete="CASCADE"), nullable=False
    )
    component: Mapped[str] = mapped_column(String(100), nullable=False)
    decision: Mapped[str] = mapped_column(Text, nullable=False)
    rationale: Mapped[str] = mapped_column(Text, nullable=True)
    alternatives: Mapped[list] = mapped_column(JSONB, default=list)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    system: Mapped["System"] = relationship(back_populates="decisions")


class SystemVersion(Base):
    """A snapshot of a system design at a point in time."""

    __tablename__ = "system_versions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    system_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("systems.id", ondelete="CASCADE"), nullable=False
    )
    version_number: Mapped[int] = mapped_column(Integer, nullable=False)
    snapshot: Mapped[dict] = mapped_column(JSONB, nullable=False)  # Full graph + sections snapshot
    change_description: Mapped[str] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    system: Mapped["System"] = relationship(back_populates="versions")
