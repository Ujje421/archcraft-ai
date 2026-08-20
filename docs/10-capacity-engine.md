# 10 — Capacity Engine

> Real computation engine — NO LLM arithmetic. Deterministic, testable, accurate.

---

## Why a Dedicated Engine?

LLMs are terrible at math. Ask ChatGPT to calculate "30M × 50 / 86400" and it might give you three different answers across three attempts.

The Capacity Engine is a **pure Python calculation module** with:
- Deterministic results
- Unit tests for every formula
- No LLM dependency
- Sub-millisecond execution

---

## Input Parameters

```python
@dataclass
class CapacityParams:
    """User-provided parameters for capacity estimation."""
    
    # Users
    total_users: int                    # Total registered users
    dau: int                            # Daily Active Users
    dau_ratio: float = 0.3             # DAU / Total (if DAU not provided)
    
    # Request patterns
    requests_per_user_per_day: int = 50
    read_write_ratio: float = 10.0      # 10:1 reads to writes
    
    # Data
    avg_request_payload_kb: float = 5.0
    avg_response_payload_kb: float = 50.0
    avg_object_size_mb: float = 1.0     # For uploads (images, videos, etc.)
    objects_per_user_per_day: float = 0.1  # How many objects uploaded
    
    # Traffic shape
    peak_multiplier: float = 5.0        # Peak = average × this
    growth_rate_monthly: float = 0.05   # 5% month-over-month
    
    # SLA
    target_availability: float = 99.99  # Percentage
    max_latency_ms: int = 200           # P99 target
```

---

## Output

```python
@dataclass
class CapacityEstimate:
    """Calculated capacity metrics."""
    
    # Request metrics
    total_requests_per_day: int
    read_requests_per_day: int
    write_requests_per_day: int
    average_rps: float
    peak_rps: float
    read_rps: float
    write_rps: float
    peak_read_rps: float
    peak_write_rps: float
    
    # Storage metrics
    daily_data_ingestion_gb: float
    monthly_storage_gb: float
    yearly_storage_tb: float
    storage_3_year_tb: float
    
    # Bandwidth metrics
    ingress_bandwidth_mbps: float
    egress_bandwidth_mbps: float
    peak_egress_bandwidth_mbps: float
    
    # Memory metrics
    cache_size_gb: float               # Estimated cache needed (20% of hot data)
    session_memory_gb: float           # Memory for active sessions
    
    # Infrastructure recommendations
    recommendations: InfraRecommendation
    
    # Formulas used (for transparency)
    formulas: list[Formula]
```

---

## Calculation Formulas

```python
class CapacityEngine:
    """Deterministic capacity calculation engine."""
    
    def calculate(self, params: CapacityParams) -> CapacityEstimate:
        # ═══════════════════════════════════════════
        # REQUEST CALCULATIONS
        # ═══════════════════════════════════════════
        
        dau = params.dau or int(params.total_users * params.dau_ratio)
        
        total_requests_per_day = dau * params.requests_per_user_per_day
        # Example: 30M × 50 = 1.5B requests/day
        
        read_ratio = params.read_write_ratio / (1 + params.read_write_ratio)
        write_ratio = 1 / (1 + params.read_write_ratio)
        
        read_requests_per_day = int(total_requests_per_day * read_ratio)
        write_requests_per_day = int(total_requests_per_day * write_ratio)
        
        average_rps = total_requests_per_day / 86400
        # Example: 1.5B / 86400 ≈ 17,361 RPS
        
        peak_rps = average_rps * params.peak_multiplier
        # Example: 17,361 × 5 ≈ 86,805 RPS
        
        read_rps = average_rps * read_ratio
        write_rps = average_rps * write_ratio
        peak_read_rps = peak_rps * read_ratio
        peak_write_rps = peak_rps * write_ratio
        
        # ═══════════════════════════════════════════
        # STORAGE CALCULATIONS
        # ═══════════════════════════════════════════
        
        # Data from API requests (metadata, text)
        daily_api_data_gb = (
            total_requests_per_day * params.avg_request_payload_kb / 1024 / 1024
        )
        
        # Object uploads (images, videos, files)
        daily_object_data_gb = (
            dau * params.objects_per_user_per_day * params.avg_object_size_mb / 1024
        )
        
        daily_data_ingestion_gb = daily_api_data_gb + daily_object_data_gb
        monthly_storage_gb = daily_data_ingestion_gb * 30
        yearly_storage_tb = monthly_storage_gb * 12 / 1024
        storage_3_year_tb = yearly_storage_tb * 3
        
        # ═══════════════════════════════════════════
        # BANDWIDTH CALCULATIONS
        # ═══════════════════════════════════════════
        
        # Ingress: data coming in
        ingress_bandwidth_mbps = (
            average_rps * params.avg_request_payload_kb * 8 / 1024
        )
        
        # Egress: data going out (responses)
        egress_bandwidth_mbps = (
            average_rps * params.avg_response_payload_kb * 8 / 1024
        )
        
        peak_egress_bandwidth_mbps = egress_bandwidth_mbps * params.peak_multiplier
        
        # ═══════════════════════════════════════════
        # MEMORY CALCULATIONS
        # ═══════════════════════════════════════════
        
        # Cache: assume 20% of daily data is "hot"
        hot_data_ratio = 0.20
        cache_size_gb = daily_data_ingestion_gb * hot_data_ratio
        
        # Sessions: ~1KB per active session, assume 10% of DAU concurrent
        concurrent_users = dau * 0.10
        session_memory_gb = concurrent_users * 1 / 1024 / 1024  # 1KB per session
        
        # ═══════════════════════════════════════════
        # INFRASTRUCTURE RECOMMENDATIONS
        # ═══════════════════════════════════════════
        
        recommendations = self._recommend_infrastructure(
            peak_rps=peak_rps,
            peak_write_rps=peak_write_rps,
            peak_read_rps=peak_read_rps,
            cache_size_gb=cache_size_gb,
            monthly_storage_gb=monthly_storage_gb,
            dau=dau,
        )
        
        return CapacityEstimate(...)
    
    def _recommend_infrastructure(self, **metrics) -> InfraRecommendation:
        """Recommend infrastructure based on calculated metrics."""
        
        peak_rps = metrics["peak_rps"]
        peak_write_rps = metrics["peak_write_rps"]
        
        # API instances: assume ~2000 RPS per instance
        rps_per_instance = 2000
        min_api_instances = max(2, math.ceil(peak_rps / rps_per_instance))
        max_api_instances = min_api_instances * 2  # Headroom
        
        # Database type
        if peak_write_rps < 5000:
            db_type = "single_with_replicas"
            db_replicas = max(1, math.ceil(metrics["peak_read_rps"] / 10000))
        elif peak_write_rps < 50000:
            db_type = "replicated"
            db_replicas = max(3, math.ceil(metrics["peak_read_rps"] / 10000))
        else:
            db_type = "sharded"
            db_replicas = max(3, math.ceil(metrics["peak_read_rps"] / 10000))
        
        # Cache needed?
        cache_needed = peak_rps > 1000 or metrics["cache_size_gb"] > 1
        
        # Queue needed?
        queue_needed = peak_write_rps > 5000 or metrics["dau"] > 1_000_000
        
        # CDN needed?
        cdn_needed = metrics["dau"] > 100_000
        
        # Load balancer
        lb_needed = min_api_instances > 1
        
        return InfraRecommendation(
            api_instances_min=min_api_instances,
            api_instances_max=max_api_instances,
            database_type=db_type,
            database_replicas=db_replicas,
            cache_needed=cache_needed,
            cache_size_gb=math.ceil(metrics["cache_size_gb"]),
            queue_needed=queue_needed,
            cdn_needed=cdn_needed,
            load_balancer_needed=lb_needed,
        )
```

---

## Formula Transparency

Every calculation is returned with its formula for display:

```python
@dataclass
class Formula:
    name: str
    formula: str
    variables: dict[str, str]
    result: str

# Example output
formulas = [
    Formula(
        name="Average RPS",
        formula="total_requests_per_day / 86,400",
        variables={"total_requests_per_day": "1,500,000,000"},
        result="17,361 RPS"
    ),
    Formula(
        name="Peak RPS",
        formula="average_rps × peak_multiplier",
        variables={"average_rps": "17,361", "peak_multiplier": "5"},
        result="86,805 RPS"
    ),
]
```

This allows the frontend to show the user **exactly how every number was calculated**.

---

## Growth Projections

```python
def project_growth(self, estimate: CapacityEstimate, months: int = 36) -> list[GrowthPoint]:
    """Project capacity metrics over time with monthly growth."""
    
    points = []
    for month in range(months + 1):
        growth = (1 + self.params.growth_rate_monthly) ** month
        points.append(GrowthPoint(
            month=month,
            dau=int(self.params.dau * growth),
            rps=estimate.average_rps * growth,
            peak_rps=estimate.peak_rps * growth,
            storage_tb=estimate.monthly_storage_gb * month / 1024,
        ))
    return points
```

---

## Unit Tests

```python
# tests/test_engines/test_capacity.py

def test_basic_calculation():
    engine = CapacityEngine()
    result = engine.calculate(CapacityParams(
        total_users=100_000_000,
        dau=30_000_000,
        requests_per_user_per_day=50,
    ))
    
    assert result.total_requests_per_day == 1_500_000_000
    assert abs(result.average_rps - 17361.11) < 1
    assert abs(result.peak_rps - 86805.56) < 1

def test_storage_calculation():
    engine = CapacityEngine()
    result = engine.calculate(CapacityParams(
        total_users=10_000_000,
        dau=3_000_000,
        avg_object_size_mb=500,  # Video uploads
        objects_per_user_per_day=0.001,  # 0.1% upload daily
    ))
    
    # 3M × 0.001 × 500MB = 1,500 GB/day ≈ 1.46 TB/day
    assert abs(result.daily_data_ingestion_gb - 1464.84) < 10

def test_recommendations_single_db():
    engine = CapacityEngine()
    result = engine.calculate(CapacityParams(
        total_users=100_000,
        dau=30_000,
        requests_per_user_per_day=20,
    ))
    
    assert result.recommendations.database_type == "single_with_replicas"
    assert result.recommendations.cache_needed is False

def test_recommendations_sharded_db():
    engine = CapacityEngine()
    result = engine.calculate(CapacityParams(
        total_users=500_000_000,
        dau=100_000_000,
        requests_per_user_per_day=100,
        read_write_ratio=5.0,
    ))
    
    assert result.recommendations.database_type == "sharded"
    assert result.recommendations.cache_needed is True
    assert result.recommendations.queue_needed is True
    assert result.recommendations.cdn_needed is True
```

---

## Related Documents

- [02-system-design-schema.md](./02-system-design-schema.md) — Section 5: Capacity Estimation
- [07-ai-engine.md](./07-ai-engine.md) — How AI uses capacity data
- [11-cost-engine.md](./11-cost-engine.md) — Cost uses capacity as input
