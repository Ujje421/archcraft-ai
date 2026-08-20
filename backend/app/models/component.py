"""Component Knowledge Base ORM models."""

import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


class Component(Base):
    """A known infrastructure component (e.g., PostgreSQL, Kafka, Redis).

    This is the knowledge base — not tied to any specific system design,
    but referenced by ArchNode.technology.
    """

    __tablename__ = "components"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    slug: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    category: Mapped[str] = mapped_column(String(50), nullable=False)  # database, cache, queue, etc.
    icon: Mapped[str] = mapped_column(String(10), nullable=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)

    # Deep knowledge
    supports: Mapped[list] = mapped_column(JSONB, default=list)
    limitations: Mapped[list] = mapped_column(JSONB, default=list)
    when_to_use: Mapped[list] = mapped_column(JSONB, default=list)
    when_not_to_use: Mapped[list] = mapped_column(JSONB, default=list)
    scaling: Mapped[dict] = mapped_column(JSONB, default=dict)
    failure_modes: Mapped[list] = mapped_column(JSONB, default=list)
    cost_model: Mapped[dict] = mapped_column(JSONB, default=dict)
    interview_questions: Mapped[list] = mapped_column(JSONB, default=list)
    production_config: Mapped[dict] = mapped_column(JSONB, default=dict)
    metrics: Mapped[dict] = mapped_column(JSONB, default=dict)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # Relationships
    alternatives: Mapped[list["ComponentAlternative"]] = relationship(
        back_populates="component", cascade="all, delete-orphan"
    )


class ComponentAlternative(Base):
    """An alternative technology for a component (e.g., Redis vs Memcached)."""

    __tablename__ = "component_alternatives"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    component_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("components.id", ondelete="CASCADE"), nullable=False
    )
    alt_slug: Mapped[str] = mapped_column(String(100), nullable=False)  # slug of the alternative
    comparison: Mapped[str] = mapped_column(Text, nullable=True)         # Why you'd pick one over the other
    score: Mapped[int] = mapped_column(Integer, default=0)               # Relative fitness score

    # Relationships
    component: Mapped["Component"] = relationship(back_populates="alternatives")
