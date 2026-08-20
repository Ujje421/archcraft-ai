# 11 — Cost Engine

> Infrastructure cost estimation based on architecture components and capacity.

---

## Overview

The Cost Engine takes an architecture graph + capacity estimate and produces a per-component monthly cost breakdown.

```
Architecture Graph + Capacity Estimate
              ↓
         Cost Engine
              ↓
    Per-Component Cost Breakdown
              ↓
    Optimization Suggestions
```

---

## Input

```python
@dataclass
class CostInput:
    graph: ArchitectureGraph          # Nodes + connections
    capacity: CapacityEstimate        # From Capacity Engine
    cloud_provider: str = "aws"       # aws, gcp, azure
    region: str = "us-east-1"
    reserved_instances: bool = False  # Use reserved pricing?
```

---

## Output

```python
@dataclass
class CostEstimate:
    total_monthly: float
    currency: str = "USD"
    
    breakdown: list[ComponentCost]
    
    # Summary by category
    by_category: dict[str, float]  # { "compute": 4200, "database": 3100, ... }
    
    # Optimization
    optimization: CostOptimization | None = None

@dataclass
class ComponentCost:
    node_id: str                     # Architecture graph node ID
    component: str                   # "PostgreSQL", "Redis", etc.
    category: str                    # "compute", "database", "cache", etc.
    monthly_cost: float
    details: str                     # "3× r6g.xlarge instances"
    line_items: list[LineItem]       # Detailed pricing breakdown

@dataclass
class LineItem:
    item: str                        # "Compute (r6g.xlarge)"
    quantity: int                    # 3
    unit_cost: float                 # 350
    total: float                     # 1050
```

---

## Pricing Data

Stored as static YAML files updated periodically:

```yaml
# knowledge/pricing/aws.yaml

compute:
  instances:
    t3_micro:    { vcpu: 2,  ram_gb: 1,   cost_hourly: 0.0104 }
    t3_medium:   { vcpu: 2,  ram_gb: 4,   cost_hourly: 0.0416 }
    m6g_large:   { vcpu: 2,  ram_gb: 8,   cost_hourly: 0.077 }
    m6g_xlarge:  { vcpu: 4,  ram_gb: 16,  cost_hourly: 0.154 }
    m6g_2xlarge: { vcpu: 8,  ram_gb: 32,  cost_hourly: 0.308 }
    m6g_4xlarge: { vcpu: 16, ram_gb: 64,  cost_hourly: 0.616 }
    c6g_large:   { vcpu: 2,  ram_gb: 4,   cost_hourly: 0.068 }
    c6g_xlarge:  { vcpu: 4,  ram_gb: 8,   cost_hourly: 0.136 }
    r6g_xlarge:  { vcpu: 4,  ram_gb: 32,  cost_hourly: 0.201 }
    r6g_4xlarge: { vcpu: 16, ram_gb: 128, cost_hourly: 0.806 }

database:
  rds_postgresql:
    db_t3_medium:   { vcpu: 2,  ram_gb: 4,   cost_hourly: 0.068 }
    db_r6g_large:   { vcpu: 2,  ram_gb: 16,  cost_hourly: 0.131 }
    db_r6g_xlarge:  { vcpu: 4,  ram_gb: 32,  cost_hourly: 0.261 }
    db_r6g_2xlarge: { vcpu: 8,  ram_gb: 64,  cost_hourly: 0.522 }
    db_r6g_4xlarge: { vcpu: 16, ram_gb: 128, cost_hourly: 1.044 }
    storage_per_gb: 0.115
    iops_included: 3000
    iops_per_extra: 0.10
    multi_az_multiplier: 2.0

cache:
  elasticache_redis:
    cache_t3_medium:  { ram_gb: 3,   cost_hourly: 0.068 }
    cache_r6g_large:  { ram_gb: 13,  cost_hourly: 0.166 }
    cache_r6g_xlarge: { ram_gb: 26,  cost_hourly: 0.332 }
    cluster_mode_multiplier: 1.0  # No extra cost for cluster mode

messaging:
  msk_kafka:
    kafka_m5_large:    { cost_hourly: 0.21 }
    kafka_m5_2xlarge:  { cost_hourly: 0.42 }
    storage_per_gb: 0.10

storage:
  s3:
    standard_per_gb: 0.023
    infrequent_per_gb: 0.0125
    glacier_per_gb: 0.004
    put_per_1000: 0.005
    get_per_1000: 0.0004
    transfer_per_gb: 0.09  # First 10TB

cdn:
  cloudfront:
    transfer_per_gb: 0.085  # First 10TB
    requests_per_10000: 0.01

load_balancer:
  alb:
    base_monthly: 22.27  # $16.20 + LCU
    per_lcu_hourly: 0.008
```

---

## Cost Calculation Logic

```python
class CostEngine:
    
    def estimate(self, input: CostInput) -> CostEstimate:
        breakdown = []
        
        for node in input.graph.nodes:
            cost = self._calculate_node_cost(node, input.capacity, input.cloud_provider)
            breakdown.append(cost)
        
        total = sum(c.monthly_cost for c in breakdown)
        
        by_category = {}
        for c in breakdown:
            by_category[c.category] = by_category.get(c.category, 0) + c.monthly_cost
        
        return CostEstimate(
            total_monthly=round(total, 2),
            breakdown=breakdown,
            by_category=by_category,
        )
    
    def _calculate_node_cost(self, node, capacity, provider) -> ComponentCost:
        match node.type:
            case "service" | "api_gateway":
                return self._cost_compute(node, capacity, provider)
            case "database":
                return self._cost_database(node, capacity, provider)
            case "cache":
                return self._cost_cache(node, capacity, provider)
            case "message_queue":
                return self._cost_queue(node, capacity, provider)
            case "object_storage":
                return self._cost_storage(node, capacity, provider)
            case "cdn":
                return self._cost_cdn(node, capacity, provider)
            case "load_balancer":
                return self._cost_lb(node, capacity, provider)
            case "monitoring":
                return self._cost_monitoring(node, capacity, provider)
            case _:
                return ComponentCost(node_id=node.id, component=node.technology,
                                    category="other", monthly_cost=0, details="N/A", line_items=[])
    
    def _cost_compute(self, node, capacity, provider) -> ComponentCost:
        """Calculate compute cost based on required RPS."""
        
        instances = capacity.recommendations.api_instances_min
        # Select instance type based on required throughput
        instance_type = self._select_instance(capacity.peak_rps, instances)
        
        hourly_cost = self.pricing[provider]["compute"]["instances"][instance_type]["cost_hourly"]
        monthly_cost = hourly_cost * 730 * instances  # 730 hours/month
        
        return ComponentCost(
            node_id=node.id,
            component=node.technology,
            category="compute",
            monthly_cost=round(monthly_cost, 2),
            details=f"{instances}× {instance_type}",
            line_items=[
                LineItem(item=f"Compute ({instance_type})", quantity=instances,
                        unit_cost=round(hourly_cost * 730, 2), total=round(monthly_cost, 2))
            ]
        )
    
    def _cost_database(self, node, capacity, provider) -> ComponentCost:
        """Calculate database cost based on write throughput and storage."""
        
        line_items = []
        
        # Instance cost
        replicas = capacity.recommendations.database_replicas
        instance_type = self._select_db_instance(capacity.peak_write_rps)
        hourly = self.pricing[provider]["database"]["rds_postgresql"][instance_type]["cost_hourly"]
        instance_cost = hourly * 730 * (1 + replicas)  # Primary + replicas
        line_items.append(LineItem(
            item=f"Primary ({instance_type})", quantity=1,
            unit_cost=round(hourly * 730, 2), total=round(hourly * 730, 2)
        ))
        if replicas > 0:
            line_items.append(LineItem(
                item=f"Read Replicas ({instance_type})", quantity=replicas,
                unit_cost=round(hourly * 730, 2), total=round(hourly * 730 * replicas, 2)
            ))
        
        # Storage cost
        storage_gb = capacity.monthly_storage_gb * 0.3  # ~30% of total is DB data
        storage_cost = storage_gb * self.pricing[provider]["database"]["rds_postgresql"]["storage_per_gb"]
        line_items.append(LineItem(
            item="Storage (gp3)", quantity=int(storage_gb),
            unit_cost=0.115, total=round(storage_cost, 2)
        ))
        
        total = instance_cost + storage_cost
        
        return ComponentCost(
            node_id=node.id,
            component=node.technology,
            category="database",
            monthly_cost=round(total, 2),
            details=f"1 primary + {replicas} replicas ({instance_type}), {int(storage_gb)}GB",
            line_items=line_items,
        )
```

---

## Cost Optimization

```python
def optimize(self, estimate: CostEstimate, target_budget: float | None = None) -> CostOptimization:
    """Suggest cost optimizations."""
    
    suggestions = []
    potential_savings = 0
    
    # 1. Reserved Instances (30-40% savings on compute)
    compute_cost = estimate.by_category.get("compute", 0)
    if compute_cost > 500:
        savings = compute_cost * 0.35
        suggestions.append(OptimizationSuggestion(
            category="compute",
            suggestion="Use Reserved Instances (1-year)",
            savings=savings,
            risk="Reduced flexibility if workload changes",
        ))
        potential_savings += savings
    
    # 2. Spot instances for workers
    # 3. S3 lifecycle policies
    # 4. Right-size over-provisioned instances
    # 5. Cache to reduce database load (and cost)
    # 6. Reduce Kafka retention
    # ...
    
    optimized_total = estimate.total_monthly - potential_savings
    
    return CostOptimization(
        current_cost=estimate.total_monthly,
        optimized_cost=round(optimized_total, 2),
        savings_percentage=round(potential_savings / estimate.total_monthly * 100, 1),
        suggestions=suggestions,
    )
```

---

## Dynamic Recalculation

When the user changes parameters:

```
User changes: Users 10M → 100M
  → Capacity Engine recalculates
  → Cost Engine recalculates with new capacity
  → Frontend shows: $2,100/month → $12,100/month
  → Diff: +477% cost increase
```

---

## Related Documents

- [10-capacity-engine.md](./10-capacity-engine.md) — Capacity provides input to cost
- [09-component-knowledge-base.md](./09-component-knowledge-base.md) — Component cost models
- [02-system-design-schema.md](./02-system-design-schema.md) — Section 21: Cost Estimation
