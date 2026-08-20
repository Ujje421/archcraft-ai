"""Capacity Engine unit tests — verifying deterministic math."""

from app.engines.capacity_engine import calculate_capacity
from app.schemas.capacity import CapacityInput


def test_basic_capacity_calculation():
    """Test capacity calculation with standard YouTube-scale parameters."""
    input_data = CapacityInput(
        total_users=100_000_000,
        dau=30_000_000,
        requests_per_user_per_day=50,
        read_write_ratio=10.0,
        avg_request_payload_kb=5.0,
        avg_object_size_mb=1.0,
        peak_multiplier=5.0,
        data_retention_years=5,
    )

    result = calculate_capacity(input_data)

    # Traffic
    assert result.total_requests_per_day == 1_500_000_000
    assert round(result.average_rps, 2) == 17361.11
    assert round(result.peak_rps, 2) == 86805.56

    # Read/Write split (10:1 ratio)
    assert result.read_rps > result.write_rps
    assert round(result.read_rps + result.write_rps, 2) == round(result.average_rps, 2)

    # Storage should be positive
    assert result.daily_data_ingestion_gb > 0
    assert result.monthly_storage_gb > 0
    assert result.yearly_storage_tb > 0
    assert result.total_storage_tb > 0

    # Bandwidth should be positive
    assert result.incoming_bandwidth_mbps > 0
    assert result.outgoing_bandwidth_mbps > 0

    # Cache
    assert result.cache_size_gb > 0

    # Recommendations
    assert result.recommendations.api_instances_min >= 2  # HA minimum
    assert result.recommendations.api_instances_max > result.recommendations.api_instances_min
    assert result.recommendations.cache_needed is True
    assert result.recommendations.cdn_needed is True
    assert result.recommendations.queue_needed is True

    # Formulas should be populated
    assert len(result.formulas) >= 5


def test_small_app_capacity():
    """Test capacity calculation for a small application (1K users)."""
    input_data = CapacityInput(
        total_users=1000,
        dau=200,
        requests_per_user_per_day=20,
        read_write_ratio=5.0,
        avg_request_payload_kb=2.0,
        avg_object_size_mb=0.5,
        peak_multiplier=3.0,
        data_retention_years=1,
    )

    result = calculate_capacity(input_data)

    assert result.total_requests_per_day == 4000
    assert result.average_rps < 1  # Very low traffic
    assert result.recommendations.database_type == "single"
    assert result.recommendations.database_replicas == 1
    assert result.recommendations.cache_needed is False
    assert result.recommendations.cdn_needed is False


def test_read_write_ratio_affects_split():
    """Test that different read/write ratios produce correct splits."""
    # 100:1 ratio (read-heavy)
    input_high_read = CapacityInput(
        total_users=1_000_000,
        dau=500_000,
        requests_per_user_per_day=10,
        read_write_ratio=100.0,
    )
    result_high = calculate_capacity(input_high_read)
    assert result_high.read_rps > result_high.write_rps * 50

    # 1:1 ratio (equal)
    input_equal = CapacityInput(
        total_users=1_000_000,
        dau=500_000,
        requests_per_user_per_day=10,
        read_write_ratio=1.0,
    )
    result_equal = calculate_capacity(input_equal)
    assert abs(result_equal.read_rps - result_equal.write_rps) < 1


def test_database_recommendation_scaling():
    """Test that database recommendations scale with load."""
    # Low load → single
    low = calculate_capacity(CapacityInput(total_users=1000, dau=100, requests_per_user_per_day=10))
    assert low.recommendations.database_type == "single"

    # Medium load → replicated
    medium = calculate_capacity(CapacityInput(total_users=10_000_000, dau=3_000_000, requests_per_user_per_day=50))
    assert medium.recommendations.database_type in ("replicated", "sharded")

    # High load → sharded
    high = calculate_capacity(CapacityInput(
        total_users=1_000_000_000, dau=300_000_000, requests_per_user_per_day=100, read_write_ratio=2.0,
    ))
    assert high.recommendations.database_type == "sharded"


def test_formulas_are_human_readable():
    """Test that formulas contain human-readable explanations."""
    result = calculate_capacity(CapacityInput(total_users=1_000_000, dau=500_000))
    for formula in result.formulas:
        assert formula.name, "Formula must have a name"
        assert formula.formula, "Formula must have the calculation"
        assert formula.result, "Formula must have the result"
