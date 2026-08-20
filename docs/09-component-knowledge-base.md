# 09 — Component Knowledge Base

> A structured, reusable library of infrastructure components that powers AI recommendations, the component explorer, and the trade-off engine.

---

## Overview

Every technology in the knowledge base has standardized metadata:

```json
{
  "slug": "kafka",
  "name": "Apache Kafka",
  "category": "messaging",
  "icon": "📨",
  "description": "Distributed event streaming platform for high-throughput, real-time data pipelines.",
  "supports": ["event_streaming", "high_throughput", "async_processing", "event_replay", "pub_sub"],
  "limitations": ["operational_complexity", "ordering_constraints", "storage_cost"],
  "when_to_use": [
    "High-throughput event streaming (100K+ events/sec)",
    "Event sourcing and replay",
    "Multiple consumers need the same events",
    "Decoupling microservices"
  ],
  "when_not_to_use": [
    "Simple task queues (use RabbitMQ or SQS)",
    "Low-volume messaging (< 1000 events/sec)",
    "When you need complex routing (use RabbitMQ)"
  ],
  "scaling": {
    "horizontal": "Add partitions and brokers",
    "max_throughput": "Millions of events/sec per cluster",
    "partition_strategy": "By entity ID for ordering"
  },
  "failure_modes": [
    {
      "scenario": "Broker failure",
      "impact": "Partitions on that broker unavailable until reassigned",
      "mitigation": "Replication factor ≥ 3, ISR-based leader election",
      "rto": "< 30 seconds"
    },
    {
      "scenario": "Consumer lag",
      "impact": "Processing delay, potential data loss if retention exceeded",
      "mitigation": "Monitor consumer lag, auto-scale consumers, alert on threshold"
    },
    {
      "scenario": "ZooKeeper failure (legacy)",
      "impact": "No metadata operations, cluster still serves existing data",
      "mitigation": "Use KRaft mode (ZooKeeper-less), ZK ensemble with 3+ nodes"
    }
  ],
  "cost_model": {
    "type": "cluster",
    "base_cost_monthly": 500,
    "per_broker_monthly": 200,
    "storage_per_gb_monthly": 0.10,
    "managed_service": {
      "aws_msk": { "base": 700, "per_broker": 300 },
      "confluent_cloud": { "base": 0, "per_cku": 1200 }
    }
  },
  "interview_questions": [
    "Why Kafka over RabbitMQ?",
    "How does Kafka ensure ordering?",
    "What is a consumer group?",
    "How does Kafka handle partition rebalancing?",
    "What is ISR (In-Sync Replica)?",
    "How would you handle exactly-once delivery?",
    "What happens when a consumer falls behind?"
  ],
  "production_config": {
    "replication_factor": 3,
    "min_isr": 2,
    "retention_hours": 168,
    "default_partitions": 12,
    "acks": "all"
  }
}
```

---

## Component Categories

### Infrastructure

| Slug | Name | Icon |
|---|---|---|
| `load_balancer` | Load Balancer | ⚖️ |
| `api_gateway` | API Gateway | 🚪 |
| `cdn` | Content Delivery Network | 🌐 |
| `dns` | DNS | 🔗 |
| `waf` | Web Application Firewall | 🛡️ |
| `reverse_proxy` | Reverse Proxy | 🔄 |

### Compute

| Slug | Name | Icon |
|---|---|---|
| `vm` | Virtual Machine | 🖥️ |
| `container` | Container (Docker) | 📦 |
| `kubernetes` | Kubernetes | ☸️ |
| `serverless` | Serverless (Lambda/Cloud Functions) | ⚡ |
| `worker` | Background Worker | 👷 |

### Databases

| Slug | Name | Icon |
|---|---|---|
| `postgresql` | PostgreSQL | 🐘 |
| `mysql` | MySQL | 🐬 |
| `mongodb` | MongoDB | 🍃 |
| `dynamodb` | DynamoDB | ⚡ |
| `cassandra` | Apache Cassandra | 👁️ |
| `redis` | Redis | 🔴 |
| `elasticsearch` | Elasticsearch | 🔍 |
| `cockroachdb` | CockroachDB | 🪳 |
| `neo4j` | Neo4j | 🕸️ |
| `clickhouse` | ClickHouse | 🏠 |

### Messaging

| Slug | Name | Icon |
|---|---|---|
| `kafka` | Apache Kafka | 📨 |
| `rabbitmq` | RabbitMQ | 🐇 |
| `sqs` | Amazon SQS | 📬 |
| `pubsub` | Google Pub/Sub | 📡 |
| `nats` | NATS | ⚡ |
| `redis_streams` | Redis Streams | 🔴 |

### Storage

| Slug | Name | Icon |
|---|---|---|
| `s3` | Amazon S3 | 🪣 |
| `gcs` | Google Cloud Storage | ☁️ |
| `azure_blob` | Azure Blob Storage | 🔷 |
| `minio` | MinIO | 📁 |

### Observability

| Slug | Name | Icon |
|---|---|---|
| `prometheus` | Prometheus | 🔥 |
| `grafana` | Grafana | 📊 |
| `opentelemetry` | OpenTelemetry | 🔭 |
| `elk` | ELK Stack | 📋 |
| `datadog` | Datadog | 🐕 |
| `pagerduty` | PagerDuty | 🚨 |

### Security

| Slug | Name | Icon |
|---|---|---|
| `oauth` | OAuth 2.0 / OIDC | 🔐 |
| `jwt` | JSON Web Tokens | 🎫 |
| `vault` | HashiCorp Vault | 🔒 |
| `rate_limiter` | Rate Limiter | 🚦 |

---

## Detailed Component Example: PostgreSQL

```yaml
slug: postgresql
name: PostgreSQL
category: database
icon: 🐘
description: >
  Open-source relational database with strong ACID compliance,
  rich SQL support, and extensive ecosystem.

supports:
  - relational_data
  - acid_transactions
  - complex_queries
  - joins
  - full_text_search
  - json_support
  - geospatial (PostGIS)
  - vector_search (pgvector)
  - partitioning
  - logical_replication

limitations:
  - horizontal_scaling (limited without sharding tools)
  - write_throughput (single-writer model)
  - operational_complexity_at_scale

when_to_use:
  - Relational data with complex queries
  - ACID transactions are required
  - Data integrity is critical
  - Moderate scale (< 50K writes/sec without sharding)
  - Need for JOINs across tables
  - Full-text search (basic)
  - JSON data alongside relational data

when_not_to_use:
  - Extreme write throughput (> 100K writes/sec) — consider Cassandra
  - Simple key-value access patterns — consider DynamoDB
  - Graph data — consider Neo4j
  - Time-series data — consider TimescaleDB or ClickHouse
  - Document-first schema — consider MongoDB

scaling:
  vertical:
    max_instance: "db.r6g.16xlarge (64 vCPU, 512 GB RAM)"
    when: "First scaling step, up to ~10K writes/sec"
  horizontal_read:
    strategy: "Read replicas"
    max_replicas: 15
    replication_type: "Streaming (async or sync)"
    when: "Read-heavy workloads, > 5:1 read:write"
  horizontal_write:
    strategy: "Application-level sharding"
    shard_key_strategies:
      - "User ID (even distribution)"
      - "Geographic region"
      - "Tenant ID (multi-tenant)"
    tools: ["Citus", "pg_partman", "Application logic"]
    when: "> 50K writes/sec or > 1TB data"

failure_modes:
  - scenario: "Primary failure"
    impact: "All writes fail, reads fail if no replicas"
    mitigation: "Promote hot standby, < 30s failover"
    rto: "< 30 seconds (managed), < 5 minutes (self-managed)"
    rpo: "0 (sync replication) or < 5s (async)"
  
  - scenario: "Replication lag"
    impact: "Stale reads from replicas"
    mitigation: "Monitor lag, route critical reads to primary"
  
  - scenario: "Connection exhaustion"
    impact: "New connections rejected"
    mitigation: "PgBouncer connection pooling, max_connections tuning"
  
  - scenario: "Table bloat (dead tuples)"
    impact: "Slow queries, disk space waste"
    mitigation: "Autovacuum tuning, manual VACUUM FULL during maintenance"

cost_model:
  type: instance
  self_hosted:
    small: { vcpu: 2, ram_gb: 8, cost_monthly: 50 }
    medium: { vcpu: 8, ram_gb: 32, cost_monthly: 200 }
    large: { vcpu: 32, ram_gb: 128, cost_monthly: 800 }
  managed:
    aws_rds:
      small: { instance: "db.t3.medium", cost_monthly: 70 }
      medium: { instance: "db.r6g.xlarge", cost_monthly: 350 }
      large: { instance: "db.r6g.4xlarge", cost_monthly: 1400 }
      multi_az_multiplier: 2.0
      storage_per_gb: 0.115
    gcp_cloud_sql:
      small: { instance: "db-custom-2-8192", cost_monthly: 65 }
      medium: { instance: "db-custom-8-32768", cost_monthly: 320 }
      large: { instance: "db-custom-32-131072", cost_monthly: 1300 }

interview_questions:
  - "Why PostgreSQL over MySQL?"
  - "How does PostgreSQL handle concurrent writes?"
  - "What is MVCC?"
  - "How does VACUUM work?"
  - "When would you shard PostgreSQL?"
  - "What is the WAL (Write-Ahead Log)?"
  - "How does streaming replication work?"
  - "What connection pooling strategies exist?"
  - "How does PostgreSQL handle full-text search?"
  - "What is the difference between sync and async replication?"

production_config:
  max_connections: 200
  shared_buffers: "25% of RAM"
  effective_cache_size: "75% of RAM"
  work_mem: "64MB"
  wal_level: "replica"
  max_wal_senders: 10
  hot_standby: "on"
  checkpoint_timeout: "10min"

related_components:
  - pgbouncer  # Connection pooling
  - pgvector   # Vector similarity search
  - citus      # Distributed PostgreSQL
  - timescaledb # Time-series extension
  - postgis    # Geospatial extension
```

---

## Architecture Patterns

Each pattern is also in the knowledge base:

```yaml
slug: cqrs
name: CQRS (Command Query Responsibility Segregation)
category: pattern
description: >
  Separate read and write models for a system. Commands (writes) go
  through one model/database, queries (reads) through another.

when_to_use:
  - Read and write workloads are vastly different
  - Complex domain with different read/write models
  - Need to scale reads independently from writes
  - Event sourcing

when_not_to_use:
  - Simple CRUD applications
  - Strong consistency is always required
  - Small team (increases operational complexity)

components_involved:
  - write_database (PostgreSQL)
  - read_database (Elasticsearch, Redis, denormalized view)
  - event_bus (Kafka, to sync read model)

tradeoffs:
  pro:
    - Independent scaling of reads/writes
    - Optimized query models
    - Better performance for read-heavy systems
  con:
    - Increased complexity
    - Eventual consistency between models
    - Data synchronization challenges

related_patterns:
  - event_sourcing
  - materialized_view
```

---

## Knowledge Base Loading

```python
# knowledge/loader.py

class KnowledgeBaseLoader:
    """Load component and pattern definitions from YAML files."""
    
    async def load_all(self):
        """Load all knowledge base data into PostgreSQL."""
        
        # Load component definitions
        for category_file in Path("knowledge/components/").glob("*.yaml"):
            data = yaml.safe_load(category_file.read_text())
            for component in data["components"]:
                await self._upsert_component(component)
        
        # Load architecture patterns
        for pattern_file in Path("knowledge/patterns/").glob("*.yaml"):
            data = yaml.safe_load(pattern_file.read_text())
            await self._upsert_pattern(data)
        
        # Generate embeddings for RAG
        await self._generate_embeddings()
    
    async def _generate_embeddings(self):
        """Generate vector embeddings for all knowledge content."""
        components = await self.db.execute(select(Component))
        for comp in components:
            text = f"{comp.name}: {comp.description}. Supports: {', '.join(comp.supports)}."
            embedding = await self.embedder.embed(text)
            await self.db.execute(
                insert(KnowledgeEmbedding).values(
                    content_type="component",
                    content=text,
                    metadata={"slug": comp.slug, "category": comp.category},
                    embedding=embedding,
                )
            )
```

---

## MVP Component Count

| Category | Count | Examples |
|---|---|---|
| Infrastructure | 6 | LB, API Gateway, CDN, DNS, WAF, Reverse Proxy |
| Compute | 5 | VM, Container, K8s, Serverless, Worker |
| Databases | 10 | PostgreSQL, MySQL, MongoDB, DynamoDB, Cassandra, Redis, Elasticsearch, CockroachDB, Neo4j, ClickHouse |
| Messaging | 6 | Kafka, RabbitMQ, SQS, Pub/Sub, NATS, Redis Streams |
| Storage | 4 | S3, GCS, Azure Blob, MinIO |
| Observability | 6 | Prometheus, Grafana, OpenTelemetry, ELK, Datadog, PagerDuty |
| Security | 4 | OAuth, JWT, Vault, Rate Limiter |
| Patterns | 8+ | CQRS, Event Sourcing, Saga, Circuit Breaker, etc. |
| **Total** | **49+** | |

---

## Related Documents

- [07-ai-engine.md](./07-ai-engine.md) — How AI uses the knowledge base
- [12-tradeoff-engine.md](./12-tradeoff-engine.md) — Technology comparison
- [08-data-model.md](./08-data-model.md) — Database tables for components
