"""Validation Engine — validate architecture graph structure and correctness.

This engine checks for structural issues in the architecture graph
without relying on AI. Pure graph validation logic.

Reference: docs/06-backend-architecture.md
"""

from dataclasses import dataclass, field

from app.schemas.system import ArchitectureGraph


@dataclass
class ValidationIssue:
    """A single validation issue found in the graph."""

    severity: str       # "error", "warning", "info"
    component: str      # Which node or "graph"
    message: str
    suggestion: str = ""


@dataclass
class ValidationResult:
    """Complete validation result for an architecture graph."""

    is_valid: bool = True
    issues: list[ValidationIssue] = field(default_factory=list)
    node_count: int = 0
    connection_count: int = 0

    @property
    def error_count(self) -> int:
        return sum(1 for i in self.issues if i.severity == "error")

    @property
    def warning_count(self) -> int:
        return sum(1 for i in self.issues if i.severity == "warning")


def validate_graph(graph: ArchitectureGraph) -> ValidationResult:
    """Validate an architecture graph for structural issues.

    Checks:
    1. No empty graphs
    2. No duplicate node IDs
    3. Connections reference existing nodes
    4. No isolated nodes (nodes with zero connections)
    5. No self-referencing connections
    6. Required component types present (at least one entrypoint)
    """
    result = ValidationResult(
        node_count=len(graph.nodes),
        connection_count=len(graph.connections),
    )

    node_ids = {node.node_id for node in graph.nodes}

    # ── 1. Empty graph ──
    if not graph.nodes:
        result.issues.append(ValidationIssue(
            severity="error",
            component="graph",
            message="Architecture graph has no nodes",
            suggestion="Add at least one component to the architecture",
        ))
        result.is_valid = False
        return result

    # ── 2. Duplicate node IDs ──
    seen_ids: set[str] = set()
    for node in graph.nodes:
        if node.node_id in seen_ids:
            result.issues.append(ValidationIssue(
                severity="error",
                component=node.node_id,
                message=f"Duplicate node ID: '{node.node_id}'",
                suggestion="Each node must have a unique ID",
            ))
            result.is_valid = False
        seen_ids.add(node.node_id)

    # ── 3. Connection references ──
    for conn in graph.connections:
        if conn.source_node_id not in node_ids:
            result.issues.append(ValidationIssue(
                severity="error",
                component=conn.source_node_id,
                message=f"Connection references non-existent source node: '{conn.source_node_id}'",
                suggestion="Add the missing node or fix the connection source",
            ))
            result.is_valid = False

        if conn.target_node_id not in node_ids:
            result.issues.append(ValidationIssue(
                severity="error",
                component=conn.target_node_id,
                message=f"Connection references non-existent target node: '{conn.target_node_id}'",
                suggestion="Add the missing node or fix the connection target",
            ))
            result.is_valid = False

    # ── 4. Isolated nodes ──
    connected_nodes: set[str] = set()
    for conn in graph.connections:
        connected_nodes.add(conn.source_node_id)
        connected_nodes.add(conn.target_node_id)

    for node in graph.nodes:
        if node.node_id not in connected_nodes and len(graph.nodes) > 1:
            result.issues.append(ValidationIssue(
                severity="warning",
                component=node.node_id,
                message=f"Node '{node.label}' ({node.node_id}) has no connections",
                suggestion="Connect this node to other components or remove it",
            ))

    # ── 5. Self-referencing connections ──
    for conn in graph.connections:
        if conn.source_node_id == conn.target_node_id:
            result.issues.append(ValidationIssue(
                severity="warning",
                component=conn.source_node_id,
                message=f"Self-referencing connection on '{conn.source_node_id}'",
                suggestion="A node should not connect to itself",
            ))

    # ── 6. Entrypoint check ──
    entrypoint_types = {"load_balancer", "api_gateway", "cdn", "client"}
    has_entrypoint = any(node.type in entrypoint_types for node in graph.nodes)
    if not has_entrypoint and len(graph.nodes) > 2:
        result.issues.append(ValidationIssue(
            severity="info",
            component="graph",
            message="No entrypoint component found (load balancer, API gateway, or CDN)",
            suggestion="Consider adding a load balancer or API gateway as the system entrypoint",
        ))

    return result
