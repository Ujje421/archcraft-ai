# 15 — Failure Simulation

> Chaos Mode — break components, simulate failures, test architecture resilience.

---

## Overview

Failure Simulation (Chaos Mode) randomly or selectively breaks components in the architecture and shows the impact. This helps users understand their architecture's resilience and learn about failure handling.

---

## Chaos Mode UI

```
┌─────────────────────────────────────────────────┐
│ 🔥 Chaos Mode                          [Stop]   │
│                                                  │
│ Architecture is under attack!                    │
│                                                  │
│ ⚠️ INCIDENT: Kafka cluster unavailable           │
│                                                  │
│ Impact:                                          │
│ • Async processing halted                        │
│ • Order notifications delayed                    │
│ • Analytics pipeline stopped                     │
│ • Users affected: 23% (write operations)         │
│                                                  │
│ Metrics:                                         │
│ • RTO (Recovery Time Objective): 8 minutes       │
│ • RPO (Recovery Point Objective): 5 minutes      │
│ • Data at risk: ~40,000 unprocessed events       │
│                                                  │
│ ┌──────────────────────────────────────────────┐ │
│ │ Recommended Recovery Steps                   │ │
│ │                                              │ │
│ │ 1. Enable fallback: sync processing mode     │ │
│ │ 2. Redirect events to dead letter queue      │ │
│ │ 3. Alert on-call engineer                    │ │
│ │ 4. Restart Kafka brokers                     │ │
│ │ 5. Replay events from offset                 │ │
│ │ 6. Verify consumer group positions           │ │
│ │ 7. Monitor for event duplication             │ │
│ └──────────────────────────────────────────────┘ │
│                                                  │
│ [ Explain ] [ Fix Architecture ] [ Next Failure ]│
└─────────────────────────────────────────────────┘
```

---

## Failure Scenarios

### Scenario Categories

| Category | Examples |
|---|---|
| **Component Failure** | Database down, Cache down, Queue down |
| **Network Failure** | Service-to-service timeout, DNS failure |
| **Capacity Failure** | 10× traffic spike, disk full, connection exhaustion |
| **Data Failure** | Data corruption, replication lag, split brain |
| **Regional Failure** | Entire AZ down, region failover |
| **Dependency Failure** | Third-party API down, CDN outage |

### Scenario Database

```python
@dataclass
class FailureScenario:
    id: str
    name: str
    category: str
    severity: str                    # "low", "medium", "high", "critical"
    affected_component_type: str     # "database", "cache", "message_queue", etc.
    description: str
    impact_analysis: ImpactAnalysis
    recovery_steps: list[str]
    prevention: list[str]

@dataclass
class ImpactAnalysis:
    users_affected_percentage: float
    services_affected: list[str]
    data_at_risk: str
    rto_minutes: float
    rpo_minutes: float
    cascading_failures: list[str]    # What else breaks
```

### Pre-defined Scenarios

```yaml
scenarios:
  # ── Database ──
  - id: db_primary_failure
    name: "Primary Database Failure"
    category: component_failure
    severity: critical
    affected_component_type: database
    description: "The primary PostgreSQL instance becomes unresponsive."
    impact:
      users_affected: 100  # All write operations fail
      services_affected: ["All services requiring write access"]
      data_at_risk: "In-flight transactions (last 5 seconds)"
      rto_minutes: 2
      rpo_minutes: 0.1
      cascading: ["API returns 503 for write operations", "Queue of pending writes grows"]
    recovery:
      - "Automatic failover: promote standby replica"
      - "Update connection strings (or use connection proxy)"
      - "Verify data consistency post-failover"
      - "Rebuild failed instance as new standby"
    prevention:
      - "Multi-AZ deployment"
      - "Connection pooler (PgBouncer) with health checks"
      - "Automated failover (Patroni, RDS Multi-AZ)"

  - id: db_replication_lag
    name: "Database Replication Lag (30+ seconds)"
    category: data_failure
    severity: medium
    affected_component_type: database
    description: "Read replicas are 30+ seconds behind the primary."
    impact:
      users_affected: 80  # Stale reads
      services_affected: ["Read-heavy services"]
      rto_minutes: 5
      rpo_minutes: 0
      cascading: ["Users see stale data", "Potential read-after-write inconsistency"]
    recovery:
      - "Route critical reads to primary"
      - "Identify and kill long-running queries on replica"
      - "Check for vacuum bloat on replica"
      - "Scale up replica instance if resource-constrained"

  # ── Cache ──
  - id: cache_cluster_failure
    name: "Redis Cluster Complete Failure"
    category: component_failure
    severity: high
    affected_component_type: cache
    description: "The entire Redis cluster becomes unavailable."
    impact:
      users_affected: 30  # Higher latency, but requests still work
      services_affected: ["All cached endpoints"]
      rto_minutes: 5
      rpo_minutes: 0  # Cache is ephemeral
      cascading: ["10× load increase on database", "Potential database overload", "Thundering herd on cold cache"]
    recovery:
      - "Application falls back to database (circuit breaker)"
      - "Restart Redis cluster"
      - "Gradual cache warm-up (don't hit DB all at once)"
      - "Implement cache stampede protection (singleflight)"

  # ── Message Queue ──
  - id: kafka_broker_failure
    name: "Kafka Cluster Unavailable"
    category: component_failure
    severity: critical
    affected_component_type: message_queue
    description: "The Kafka cluster becomes unreachable."
    impact:
      users_affected: 23
      services_affected: ["Async processing", "Event-driven services"]
      data_at_risk: "~40,000 unprocessed events"
      rto_minutes: 8
      rpo_minutes: 5
      cascading: ["Notifications delayed", "Analytics pipeline halted", "Event-sourced state may be stale"]

  - id: kafka_consumer_lag
    name: "Kafka Consumer Lag: 10M Messages"
    category: capacity_failure
    severity: high
    affected_component_type: message_queue
    description: "Consumers are 10 million messages behind producers."
    impact:
      users_affected: 15
      rto_minutes: 60  # Time to catch up
      cascading: ["Delayed processing", "Potential retention overflow"]
    recovery:
      - "Scale up consumer instances"
      - "Increase consumer parallelism (more partitions)"
      - "Skip non-critical events if needed"
      - "Investigate root cause (slow consumer, resource exhaustion)"

  # ── Traffic ──
  - id: traffic_spike_20x
    name: "20× Traffic Spike"
    category: capacity_failure
    severity: critical
    affected_component_type: service
    description: "Traffic suddenly increases 20× (viral event, DDoS, flash sale)."
    impact:
      users_affected: 70
      cascading: ["Auto-scaler can't keep up", "Database connection exhaustion", "Cache miss storm", "Queue backlog"]
    recovery:
      - "Enable rate limiting"
      - "Scale up aggressively (pre-warm if possible)"
      - "Enable degraded mode (serve cached/static content)"
      - "Shed non-critical traffic"
      - "Engage CDN for static content offloading"

  # ── Regional ──
  - id: region_failure
    name: "Complete AWS Region Failure"
    category: regional_failure
    severity: critical
    affected_component_type: all
    description: "The entire primary region (us-east-1) goes offline."
    impact:
      users_affected: 100  # If single-region
      rto_minutes: 30
      rpo_minutes: 15
      cascading: ["All services down", "Data may be stale in DR region"]
    recovery:
      - "DNS failover to secondary region"
      - "Promote secondary database"
      - "Verify data consistency"
      - "Update CDN origins"
      - "Communicate with users about degraded service"
    prevention:
      - "Multi-region active-active deployment"
      - "Cross-region database replication"
      - "Regular DR drills"
```

---

## Chaos Simulation Engine

```python
class ChaosEngine:
    """Simulate failures in an architecture."""
    
    def simulate_random(self, graph: ArchitectureGraph) -> FailureSimulation:
        """Pick a random component and fail it."""
        
        # Choose a random node
        node = random.choice(graph.nodes)
        
        # Find applicable scenarios
        scenarios = self.get_scenarios_for_type(node.type)
        scenario = random.choice(scenarios)
        
        # Analyze impact on THIS specific architecture
        impact = self.analyze_impact(graph, node, scenario)
        
        return FailureSimulation(
            failed_node=node,
            scenario=scenario,
            impact=impact,
            recovery_steps=scenario.recovery,
            architecture_fix=self.suggest_fix(graph, node, scenario),
        )
    
    def simulate_specific(self, graph: ArchitectureGraph, node_id: str, scenario_id: str) -> FailureSimulation:
        """Simulate a specific failure on a specific component."""
        pass
    
    def analyze_impact(self, graph: ArchitectureGraph, failed_node: ArchNode, scenario) -> ImpactAnalysis:
        """Analyze the blast radius of a failure.
        
        1. Find all nodes that depend on the failed node
        2. Calculate cascading failures
        3. Estimate user impact
        4. Determine RTO/RPO
        """
        
        # Find dependent nodes (BFS from failed node, following reverse edges)
        dependents = self._find_dependents(graph, failed_node.id)
        
        # Check for redundancy (replicas, failover)
        has_redundancy = self._check_redundancy(graph, failed_node)
        
        # Calculate impact
        if has_redundancy:
            users_affected = scenario.impact.users_affected * 0.1  # Reduced impact
            rto = scenario.impact.rto_minutes * 0.3
        else:
            users_affected = scenario.impact.users_affected
            rto = scenario.impact.rto_minutes
        
        return ImpactAnalysis(
            users_affected_percentage=users_affected,
            services_affected=[n.label for n in dependents],
            rto_minutes=rto,
            rpo_minutes=scenario.impact.rpo_minutes,
            cascading_failures=[
                f"{n.label} becomes unavailable"
                for n in dependents
                if not self._check_redundancy(graph, n)
            ],
        )
    
    def suggest_fix(self, graph: ArchitectureGraph, failed_node: ArchNode, scenario) -> GraphDiff | None:
        """Suggest architecture improvements to prevent this failure."""
        
        suggestions = []
        
        # No replicas? Add replicas
        if failed_node.type == "database" and not self._has_replicas(graph, failed_node):
            suggestions.append(AddNode(type="database", technology=failed_node.technology, label=f"{failed_node.label} Replica"))
        
        # No cache before database?
        if failed_node.type == "database" and not self._has_cache_layer(graph, failed_node):
            suggestions.append(AddNode(type="cache", technology="Redis", label="Cache Layer"))
        
        # No circuit breaker?
        # No dead letter queue?
        # No multi-AZ?
        
        return GraphDiff(add_nodes=suggestions) if suggestions else None
```

---

## Canvas Integration

When a failure is simulated:

1. **Failed node** turns red with pulsing animation
2. **Affected nodes** turn orange/amber
3. **Unaffected nodes** dim slightly
4. **Broken connections** show as dashed red lines
5. **Working connections** remain normal

```css
.arch-node.failed {
  border-color: #ef4444;
  box-shadow: 0 0 20px rgba(239, 68, 68, 0.4);
  animation: failPulse 2s infinite;
}

.arch-node.affected {
  border-color: #f59e0b;
  box-shadow: 0 0 15px rgba(245, 158, 11, 0.3);
}

.arch-node.unaffected {
  opacity: 0.4;
}

@keyframes failPulse {
  0%, 100% { box-shadow: 0 0 20px rgba(239, 68, 68, 0.4); }
  50% { box-shadow: 0 0 30px rgba(239, 68, 68, 0.7); }
}
```

---

## Related Documents

- [02-system-design-schema.md](./02-system-design-schema.md) — Section 17: Fault Tolerance
- [13-canvas-architecture.md](./13-canvas-architecture.md) — Canvas visual states
- [09-component-knowledge-base.md](./09-component-knowledge-base.md) — Failure modes per component
