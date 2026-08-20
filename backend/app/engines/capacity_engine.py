"""Capacity Engine — deterministic capacity and infrastructure sizing calculations.

This engine does NOT use LLMs. Every number is computed from first-principles
formulas that are standard in system design interviews and production planning.

Reference: docs/10-capacity-engine.md
"""

import math

from app.schemas.capacity import (
    CapacityFormula,
    CapacityInput,
    CapacityOutput,
    InfraRecommendations,
)

# ── Constants ──
SECONDS_PER_DAY = 86_400
DAYS_PER_MONTH = 30
DAYS_PER_YEAR = 365
BYTES_PER_KB = 1024
BYTES_PER_MB = 1024 * 1024
BYTES_PER_GB = 1024 * 1024 * 1024
BYTES_PER_TB = 1024 * 1024 * 1024 * 1024

# Infrastructure sizing constants
RPS_PER_API_INSTANCE = 1000       # Typical API server capacity
MAX_DB_WRITE_RPS = 5000           # Single PostgreSQL write throughput
MAX_DB_READ_RPS = 20000           # Single PostgreSQL read throughput (with indexes)
CACHE_HIT_RATIO = 0.8             # 80% cache hit rate assumption
CACHE_HOT_DATA_PERCENT = 0.2      # 20% of data is "hot" (frequently accessed)


def calculate_capacity(input_data: CapacityInput) -> CapacityOutput:
    """Calculate all capacity metrics from input parameters.

    Returns a complete CapacityOutput with traffic, storage, bandwidth,
    cache sizing, infrastructure recommendations, and all formulas shown.
    """
    formulas: list[CapacityFormula] = []

    # ═══════════════════════════════════════════════
    # 1. TRAFFIC CALCULATIONS
    # ═══════════════════════════════════════════════

    total_requests_per_day = input_data.dau * input_data.requests_per_user_per_day
    formulas.append(CapacityFormula(
        name="Total Requests/Day",
        formula=f"{input_data.dau:,} DAU × {input_data.requests_per_user_per_day} req/user/day",
        result=f"{total_requests_per_day:,} requests/day",
    ))

    average_rps = total_requests_per_day / SECONDS_PER_DAY
    formulas.append(CapacityFormula(
        name="Average RPS",
        formula=f"{total_requests_per_day:,} / {SECONDS_PER_DAY:,} seconds",
        result=f"{average_rps:,.2f} RPS",
    ))

    peak_rps = average_rps * input_data.peak_multiplier
    formulas.append(CapacityFormula(
        name="Peak RPS",
        formula=f"{average_rps:,.2f} × {input_data.peak_multiplier}× peak multiplier",
        result=f"{peak_rps:,.2f} RPS",
    ))

    # Read/write split
    ratio = input_data.read_write_ratio
    write_rps = average_rps / (1 + ratio)
    read_rps = average_rps - write_rps
    formulas.append(CapacityFormula(
        name="Read/Write Split",
        formula=f"Ratio {ratio}:1 → Reads: {average_rps:,.2f} × {ratio}/{ratio + 1} | Writes: {average_rps:,.2f} × 1/{ratio + 1}",
        result=f"Read: {read_rps:,.2f} RPS | Write: {write_rps:,.2f} RPS",
    ))

    # ═══════════════════════════════════════════════
    # 2. STORAGE CALCULATIONS
    # ═══════════════════════════════════════════════

    # Daily write volume (only writes generate new data)
    writes_per_day = total_requests_per_day / (1 + ratio)
    daily_data_ingestion_bytes = writes_per_day * input_data.avg_object_size_mb * BYTES_PER_MB
    daily_data_ingestion_gb = daily_data_ingestion_bytes / BYTES_PER_GB
    formulas.append(CapacityFormula(
        name="Daily Data Ingestion",
        formula=f"{writes_per_day:,.0f} writes/day × {input_data.avg_object_size_mb} MB",
        result=f"{daily_data_ingestion_gb:,.2f} GB/day",
    ))

    monthly_storage_gb = daily_data_ingestion_gb * DAYS_PER_MONTH
    yearly_storage_tb = daily_data_ingestion_gb * DAYS_PER_YEAR / 1024
    total_storage_tb = yearly_storage_tb * input_data.data_retention_years
    formulas.append(CapacityFormula(
        name="Storage Growth",
        formula=f"{daily_data_ingestion_gb:,.2f} GB/day × 365 days × {input_data.data_retention_years} years",
        result=f"Monthly: {monthly_storage_gb:,.2f} GB | Yearly: {yearly_storage_tb:,.2f} TB | Total ({input_data.data_retention_years}yr): {total_storage_tb:,.2f} TB",
    ))

    # ═══════════════════════════════════════════════
    # 3. BANDWIDTH CALCULATIONS
    # ═══════════════════════════════════════════════

    incoming_bandwidth_bps = average_rps * input_data.avg_request_payload_kb * BYTES_PER_KB * 8
    incoming_bandwidth_mbps = incoming_bandwidth_bps / (1024 * 1024)

    # Outgoing is typically larger (responses include data)
    outgoing_bandwidth_mbps = incoming_bandwidth_mbps * 2  # 2x for response overhead
    formulas.append(CapacityFormula(
        name="Bandwidth",
        formula=f"{average_rps:,.2f} RPS × {input_data.avg_request_payload_kb} KB × 8 bits",
        result=f"In: {incoming_bandwidth_mbps:,.2f} Mbps | Out: {outgoing_bandwidth_mbps:,.2f} Mbps",
    ))

    # ═══════════════════════════════════════════════
    # 4. CACHE SIZING
    # ═══════════════════════════════════════════════

    # Cache the "hot" 20% of daily data
    cache_size_gb = daily_data_ingestion_gb * CACHE_HOT_DATA_PERCENT * DAYS_PER_MONTH
    cache_size_gb = max(cache_size_gb, 0.5)  # Minimum 0.5 GB
    formulas.append(CapacityFormula(
        name="Cache Size",
        formula=f"{daily_data_ingestion_gb:,.2f} GB/day × {CACHE_HOT_DATA_PERCENT * 100}% hot data × 30 days",
        result=f"{cache_size_gb:,.2f} GB",
    ))

    # ═══════════════════════════════════════════════
    # 5. INFRASTRUCTURE RECOMMENDATIONS
    # ═══════════════════════════════════════════════

    api_instances_min = max(math.ceil(average_rps / RPS_PER_API_INSTANCE), 2)  # Min 2 for HA
    api_instances_max = max(math.ceil(peak_rps / RPS_PER_API_INSTANCE), api_instances_min + 1)

    # Database strategy
    if write_rps > MAX_DB_WRITE_RPS:
        database_type = "sharded"
        database_replicas = max(math.ceil(read_rps / MAX_DB_READ_RPS), 3)
    elif read_rps > MAX_DB_READ_RPS:
        database_type = "replicated"
        database_replicas = math.ceil(read_rps / MAX_DB_READ_RPS)
    elif average_rps > 1000:
        database_type = "replicated"
        database_replicas = 2
    else:
        database_type = "single"
        database_replicas = 1

    cache_needed = average_rps > 500 or read_rps > 2000
    queue_needed = write_rps > 500 or average_rps > 5000
    cdn_needed = average_rps > 1000 or input_data.dau > 100_000

    recommendations = InfraRecommendations(
        api_instances_min=api_instances_min,
        api_instances_max=api_instances_max,
        database_type=database_type,
        database_replicas=database_replicas,
        cache_needed=cache_needed,
        cache_size_gb=round(cache_size_gb, 2),
        queue_needed=queue_needed,
        cdn_needed=cdn_needed,
    )

    formulas.append(CapacityFormula(
        name="API Instances",
        formula=f"avg {average_rps:,.0f} RPS / {RPS_PER_API_INSTANCE} RPS/instance (min 2 for HA)",
        result=f"Min: {api_instances_min} | Max: {api_instances_max}",
    ))

    formulas.append(CapacityFormula(
        name="Database Strategy",
        formula=f"Write RPS: {write_rps:,.0f} (limit: {MAX_DB_WRITE_RPS:,}) | Read RPS: {read_rps:,.0f} (limit: {MAX_DB_READ_RPS:,})",
        result=f"{database_type} with {database_replicas} replica(s)",
    ))

    # ═══════════════════════════════════════════════
    # ASSEMBLE OUTPUT
    # ═══════════════════════════════════════════════

    return CapacityOutput(
        total_requests_per_day=total_requests_per_day,
        average_rps=round(average_rps, 2),
        peak_rps=round(peak_rps, 2),
        read_rps=round(read_rps, 2),
        write_rps=round(write_rps, 2),
        daily_data_ingestion_gb=round(daily_data_ingestion_gb, 2),
        monthly_storage_gb=round(monthly_storage_gb, 2),
        yearly_storage_tb=round(yearly_storage_tb, 2),
        total_storage_tb=round(total_storage_tb, 2),
        incoming_bandwidth_mbps=round(incoming_bandwidth_mbps, 2),
        outgoing_bandwidth_mbps=round(outgoing_bandwidth_mbps, 2),
        cache_size_gb=round(cache_size_gb, 2),
        recommendations=recommendations,
        formulas=formulas,
    )
