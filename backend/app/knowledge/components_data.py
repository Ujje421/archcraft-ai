"""Component Knowledge Base — in-memory seed data for MVP.

This will be migrated to PostgreSQL in a later sprint.
For now, it serves as the single source of truth for the component explorer.

Reference: docs/09-component-knowledge-base.md
"""

COMPONENTS_DB: dict[str, dict] = {
    # ═══════════════════════════════════════════════
    # DATABASES
    # ═══════════════════════════════════════════════
    "postgresql": {
        "slug": "postgresql",
        "name": "PostgreSQL",
        "category": "database",
        "icon": "🐘",
        "description": "Open-source relational database with advanced features including JSONB, full-text search, and extensions like pgvector.",
        "supports": [
            "ACID transactions",
            "Complex joins and subqueries",
            "JSONB for semi-structured data",
            "Full-text search",
            "Materialized views",
            "Row-level security",
            "Logical replication",
            "Extensions (PostGIS, pgvector, TimescaleDB)",
        ],
        "limitations": [
            "Vertical scaling primarily (write scaling is hard)",
            "Connection overhead (use PgBouncer)",
            "VACUUM maintenance required",
            "Complex sharding (use Citus for horizontal scaling)",
        ],
        "when_to_use": [
            "Transactional data (orders, payments, users)",
            "Complex queries with joins",
            "Need for ACID guarantees",
            "Semi-structured data (JSONB)",
            "Geospatial data (PostGIS)",
            "Vector embeddings (pgvector)",
        ],
        "when_not_to_use": [
            "Simple key-value lookups at massive scale → use DynamoDB or Redis",
            "Write-heavy time-series → use TimescaleDB or InfluxDB",
            "Document-centric with no relations → use MongoDB",
            "Graph traversals → use Neo4j",
        ],
        "scaling": {
            "read_scaling": "Read replicas (streaming replication)",
            "write_scaling": "Vertical scaling, or Citus for horizontal sharding",
            "connection_pooling": "PgBouncer (recommended for > 100 connections)",
            "max_single_instance": "~50K writes/sec, ~200K reads/sec (tuned)",
        },
        "failure_modes": [
            {"mode": "Primary failure", "impact": "All writes fail", "mitigation": "Automatic failover with Patroni or RDS Multi-AZ"},
            {"mode": "Replication lag", "impact": "Stale reads from replicas", "mitigation": "Route critical reads to primary"},
            {"mode": "Connection exhaustion", "impact": "New connections rejected", "mitigation": "PgBouncer + connection limits"},
            {"mode": "Disk full", "impact": "Database goes read-only", "mitigation": "Monitoring + auto-scaling storage"},
        ],
        "cost_model": {
            "aws_rds": {"small": "$30/mo (db.t3.medium)", "medium": "$200/mo (db.r6g.large)", "large": "$800/mo (db.r6g.2xlarge)"},
            "storage": "$0.115/GB/month (gp3)",
        },
        "interview_questions": [
            "How would you handle a hot partition in PostgreSQL?",
            "Explain the difference between logical and physical replication.",
            "When would you choose PostgreSQL over DynamoDB?",
            "How does MVCC work in PostgreSQL?",
            "What's the CAP theorem trade-off for PostgreSQL?",
        ],
        "production_config": {
            "max_connections": 200,
            "shared_buffers": "25% of RAM",
            "effective_cache_size": "75% of RAM",
            "work_mem": "4MB per connection",
            "maintenance_work_mem": "512MB",
        },
    },

    "mysql": {
        "slug": "mysql",
        "name": "MySQL",
        "category": "database",
        "icon": "🐬",
        "description": "The world's most popular open-source relational database, known for simplicity and read performance.",
        "supports": ["ACID transactions (InnoDB)", "Replication (async, semi-sync, group)", "Partitioning", "JSON support"],
        "limitations": ["Weaker subquery optimization than PostgreSQL", "No native JSONB indexing", "Limited extension ecosystem"],
        "when_to_use": ["Web applications with read-heavy workloads", "WordPress/PHP ecosystems", "Simple CRUD applications"],
        "when_not_to_use": ["Complex analytical queries", "Need for advanced PostgreSQL features (CTE, window functions)"],
        "scaling": {"read_scaling": "Read replicas", "write_scaling": "Vitess for horizontal sharding"},
        "failure_modes": [{"mode": "Primary failure", "impact": "Writes stop", "mitigation": "Group replication or InnoDB Cluster"}],
        "cost_model": {"aws_rds": {"small": "$25/mo", "medium": "$180/mo", "large": "$700/mo"}},
        "interview_questions": ["How does InnoDB handle locking?", "Explain MySQL replication topologies."],
    },

    "mongodb": {
        "slug": "mongodb",
        "name": "MongoDB",
        "category": "database",
        "icon": "🍃",
        "description": "Document database storing flexible JSON-like documents (BSON). Excellent for rapid development and schema-flexible data.",
        "supports": ["Flexible schema", "Sharding", "Aggregation pipeline", "Change streams", "Atlas Search"],
        "limitations": ["No multi-document ACID until v4.0+", "Memory-hungry indexes", "Join performance (lookup)", "Eventual consistency by default"],
        "when_to_use": ["Rapidly evolving schemas", "Document-centric data (CMS, catalogs)", "Real-time analytics with aggregation pipeline"],
        "when_not_to_use": ["Highly relational data with complex joins", "Financial transactions requiring strict ACID", "Small datasets (overkill)"],
        "scaling": {"read_scaling": "Replica sets", "write_scaling": "Sharding with shard keys"},
        "failure_modes": [{"mode": "Primary election", "impact": "Writes pause for 10-12 seconds", "mitigation": "3+ replica set members"}],
        "cost_model": {"atlas": {"shared": "$0/mo", "dedicated_m10": "$60/mo", "dedicated_m30": "$300/mo"}},
        "interview_questions": ["When would you choose MongoDB over PostgreSQL?", "Explain shard key selection strategy."],
    },

    "dynamodb": {
        "slug": "dynamodb",
        "name": "Amazon DynamoDB",
        "category": "database",
        "icon": "⚡",
        "description": "Fully managed NoSQL key-value and document database with single-digit millisecond performance at any scale.",
        "supports": ["Auto-scaling", "Global tables (multi-region)", "DAX (in-memory cache)", "Streams", "TTL"],
        "limitations": ["400KB item size limit", "No ad-hoc queries (design around access patterns)", "Costly for scan-heavy workloads"],
        "when_to_use": ["High-throughput key-value lookups", "Serverless architectures", "Session storage", "IoT data"],
        "when_not_to_use": ["Complex queries with joins", "Ad-hoc analytics", "Budget-constrained small projects"],
        "scaling": {"read_scaling": "Automatic", "write_scaling": "Automatic (with provisioned or on-demand)"},
        "failure_modes": [{"mode": "Hot partition", "impact": "Throttling on specific keys", "mitigation": "Better partition key design"}],
        "cost_model": {"on_demand": "$1.25 per million writes, $0.25 per million reads", "provisioned": "$0.00065/WCU/hr"},
        "interview_questions": ["How do you model a many-to-many relationship in DynamoDB?", "Explain single-table design."],
    },

    # ═══════════════════════════════════════════════
    # CACHING
    # ═══════════════════════════════════════════════
    "redis": {
        "slug": "redis",
        "name": "Redis",
        "category": "cache",
        "icon": "🔴",
        "description": "In-memory data store used as cache, message broker, and real-time data structure server.",
        "supports": [
            "Key-value caching",
            "Pub/Sub messaging",
            "Sorted sets (leaderboards)",
            "Streams (event log)",
            "Lua scripting",
            "Cluster mode (sharding)",
            "Persistence (RDB + AOF)",
            "Rate limiting (sliding window)",
        ],
        "limitations": [
            "Data must fit in memory",
            "Single-threaded command processing",
            "Cluster mode adds complexity",
            "Persistence can cause latency spikes",
        ],
        "when_to_use": [
            "Application caching (reduce database load)",
            "Session storage",
            "Rate limiting",
            "Real-time leaderboards",
            "Pub/Sub for real-time features",
            "Distributed locks",
        ],
        "when_not_to_use": [
            "Primary database for durable data",
            "Datasets larger than available memory",
            "Complex queries (use a database)",
        ],
        "scaling": {
            "read_scaling": "Read replicas",
            "write_scaling": "Cluster mode (hash-slot based sharding)",
            "max_single_instance": "~100K ops/sec",
        },
        "failure_modes": [
            {"mode": "OOM (out of memory)", "impact": "Eviction or crash", "mitigation": "maxmemory policy + monitoring"},
            {"mode": "Cluster split-brain", "impact": "Data inconsistency", "mitigation": "Proper quorum settings"},
        ],
        "cost_model": {
            "aws_elasticache": {"small": "$15/mo (cache.t3.micro)", "medium": "$100/mo (cache.r6g.large)", "large": "$400/mo (cache.r6g.2xlarge)"},
        },
        "interview_questions": [
            "How would you implement a rate limiter with Redis?",
            "Explain the difference between Redis Pub/Sub and Kafka.",
            "How does Redis Cluster handle failover?",
            "What's the cache stampede problem and how do you solve it?",
        ],
    },

    "memcached": {
        "slug": "memcached",
        "name": "Memcached",
        "category": "cache",
        "icon": "🟢",
        "description": "Simple, high-performance distributed memory caching system. Simpler than Redis but extremely fast for key-value caching.",
        "supports": ["Key-value caching", "Multi-threaded", "Consistent hashing"],
        "limitations": ["No persistence", "No data structures (only strings)", "No pub/sub", "No clustering (client-side sharding)"],
        "when_to_use": ["Simple caching with multi-threaded performance", "Large object caching (up to 1MB)"],
        "when_not_to_use": ["Need data structures, persistence, or pub/sub → use Redis"],
        "scaling": {"read_scaling": "Add more nodes (client-side hashing)", "write_scaling": "Add more nodes"},
        "interview_questions": ["When would you pick Memcached over Redis?"],
    },

    # ═══════════════════════════════════════════════
    # MESSAGE QUEUES
    # ═══════════════════════════════════════════════
    "kafka": {
        "slug": "kafka",
        "name": "Apache Kafka",
        "category": "message_queue",
        "icon": "📨",
        "description": "Distributed event streaming platform for high-throughput, fault-tolerant, real-time data pipelines.",
        "supports": [
            "Pub/Sub messaging",
            "Event sourcing",
            "Stream processing (Kafka Streams, ksqlDB)",
            "Log compaction",
            "Exactly-once semantics",
            "Multi-datacenter replication (MirrorMaker)",
            "Schema Registry (Avro, Protobuf)",
        ],
        "limitations": [
            "Operational complexity",
            "Not ideal for low-latency request-reply",
            "Ordering only within partitions",
            "Rebalancing can cause consumer lag",
        ],
        "when_to_use": [
            "Async event processing at scale",
            "Event-driven microservices",
            "Real-time analytics pipelines",
            "Change Data Capture (CDC)",
            "Log aggregation",
        ],
        "when_not_to_use": [
            "Simple task queues → use RabbitMQ or SQS",
            "Request-reply patterns → use gRPC",
            "Low message volume (< 1000/sec) → overkill",
        ],
        "scaling": {
            "throughput": "Add partitions + brokers",
            "max_single_cluster": "Millions of messages/sec",
        },
        "failure_modes": [
            {"mode": "Broker failure", "impact": "Partitions re-assigned", "mitigation": "Replication factor ≥ 3"},
            {"mode": "Consumer lag", "impact": "Processing delays", "mitigation": "Scale consumers, increase partitions"},
        ],
        "cost_model": {
            "aws_msk": {"small": "$100/mo (kafka.t3.small × 3)", "medium": "$500/mo (kafka.m5.large × 3)"},
            "confluent_cloud": {"basic": "$0.12/GB ingress"},
        },
        "interview_questions": [
            "How does Kafka achieve exactly-once semantics?",
            "Explain Kafka's replication model.",
            "How would you handle ordering across partitions?",
            "When would you use Kafka vs RabbitMQ?",
        ],
    },

    "rabbitmq": {
        "slug": "rabbitmq",
        "name": "RabbitMQ",
        "category": "message_queue",
        "icon": "🐰",
        "description": "Reliable message broker with flexible routing, supporting AMQP, MQTT, and STOMP protocols.",
        "supports": ["Routing (direct, topic, fanout, headers)", "Dead letter queues", "Priority queues", "Message acknowledgment", "Plugins"],
        "limitations": ["Lower throughput than Kafka", "No event replay", "Message ordering not guaranteed across queues"],
        "when_to_use": ["Task queues with routing logic", "RPC-style communication", "Priority-based processing"],
        "when_not_to_use": ["High-throughput event streaming → use Kafka", "Event replay required → use Kafka"],
        "scaling": {"throughput": "Clustering + sharded queues"},
        "interview_questions": ["Compare RabbitMQ exchange types.", "When would you choose RabbitMQ over Kafka?"],
    },

    # ═══════════════════════════════════════════════
    # SEARCH
    # ═══════════════════════════════════════════════
    "elasticsearch": {
        "slug": "elasticsearch",
        "name": "Elasticsearch",
        "category": "search",
        "icon": "🔍",
        "description": "Distributed search and analytics engine based on Apache Lucene. Powers full-text search, log analytics, and observability.",
        "supports": ["Full-text search", "Aggregations", "Near real-time indexing", "Geospatial queries", "Machine learning anomaly detection"],
        "limitations": ["Not a primary database", "Split-brain risk", "Memory-intensive", "Complex cluster management"],
        "when_to_use": ["Full-text search (product search, articles)", "Log analytics (ELK stack)", "Autocomplete and suggestions"],
        "when_not_to_use": ["Primary data store → use a database", "Simple key-value lookups → use Redis"],
        "scaling": {"read_scaling": "Replica shards", "write_scaling": "Primary shards across nodes"},
        "interview_questions": ["How does Elasticsearch achieve near real-time search?", "Explain inverted indexes."],
    },

    # ═══════════════════════════════════════════════
    # LOAD BALANCERS & NETWORKING
    # ═══════════════════════════════════════════════
    "nginx": {
        "slug": "nginx",
        "name": "NGINX",
        "category": "load_balancer",
        "icon": "⚖️",
        "description": "High-performance web server and reverse proxy, commonly used as a load balancer and API gateway.",
        "supports": ["Reverse proxy", "Load balancing (round-robin, least connections, IP hash)", "SSL termination", "Rate limiting", "Static file serving"],
        "limitations": ["Configuration complexity at scale", "Limited dynamic service discovery (vs Envoy)"],
        "when_to_use": ["Reverse proxy for web applications", "SSL termination", "Load balancing across API servers"],
        "when_not_to_use": ["Service mesh with dynamic routing → use Envoy/Istio"],
        "interview_questions": ["Explain L4 vs L7 load balancing.", "How does NGINX handle 10K concurrent connections?"],
    },

    "kong": {
        "slug": "kong",
        "name": "Kong API Gateway",
        "category": "api_gateway",
        "icon": "🦍",
        "description": "Cloud-native API gateway built on NGINX/OpenResty with plugin ecosystem for auth, rate limiting, and observability.",
        "supports": ["Rate limiting", "Authentication (JWT, OAuth)", "Request transformation", "Logging", "Plugin ecosystem"],
        "limitations": ["Learning curve", "Resource overhead vs plain NGINX"],
        "when_to_use": ["Microservice architectures needing centralized API management", "Multi-tenant API platforms"],
        "when_not_to_use": ["Simple monolith → use NGINX directly"],
        "interview_questions": ["Why use an API gateway vs direct service-to-service calls?"],
    },

    # ═══════════════════════════════════════════════
    # STORAGE
    # ═══════════════════════════════════════════════
    "s3": {
        "slug": "s3",
        "name": "Amazon S3",
        "category": "object_storage",
        "icon": "🪣",
        "description": "Infinitely scalable object storage with 99.999999999% (11 nines) durability.",
        "supports": ["Object storage", "Versioning", "Lifecycle policies", "Event notifications", "Static website hosting", "Glacier archiving"],
        "limitations": ["Not a filesystem", "Eventual consistency for overwrite PUTs (now strong in most cases)", "5TB max object size"],
        "when_to_use": ["Media storage (images, videos, documents)", "Backups and archives", "Data lake storage", "Static asset hosting"],
        "when_not_to_use": ["Low-latency random access → use EBS or local SSD", "Structured queries → use a database"],
        "cost_model": {"standard": "$0.023/GB/month", "infrequent_access": "$0.0125/GB/month", "glacier": "$0.004/GB/month"},
        "interview_questions": ["How would you design a media upload pipeline with S3?", "Explain S3 storage classes."],
    },

    "cloudfront": {
        "slug": "cloudfront",
        "name": "Amazon CloudFront",
        "category": "cdn",
        "icon": "🌐",
        "description": "Global content delivery network (CDN) for low-latency delivery of static and dynamic content.",
        "supports": ["Edge caching", "SSL/TLS", "Lambda@Edge", "WebSocket support", "Real-time logs"],
        "limitations": ["Cache invalidation delay", "Cost at high traffic"],
        "when_to_use": ["Global user base", "Static asset delivery", "Video streaming", "API acceleration"],
        "when_not_to_use": ["Single-region, low-traffic apps"],
        "cost_model": {"data_transfer": "$0.085/GB (first 10TB)", "requests": "$0.01/10K HTTPS requests"},
        "interview_questions": ["How does a CDN reduce latency?", "Explain cache invalidation strategies."],
    },

    # ═══════════════════════════════════════════════
    # COMPUTE / SERVICES
    # ═══════════════════════════════════════════════
    "docker": {
        "slug": "docker",
        "name": "Docker",
        "category": "compute",
        "icon": "🐳",
        "description": "Container platform for packaging and running applications in isolated, reproducible environments.",
        "supports": ["Container isolation", "Image layers", "Docker Compose", "Multi-stage builds"],
        "limitations": ["Not a VM (shared kernel)", "Storage driver complexity", "Security (root by default)"],
        "when_to_use": ["Microservice deployment", "CI/CD pipelines", "Development environments", "Any production workload"],
        "when_not_to_use": ["GUI applications", "Heavy GPU workloads (use VMs)"],
        "interview_questions": ["Explain container vs VM.", "How does Docker layered filesystem work?"],
    },

    "kubernetes": {
        "slug": "kubernetes",
        "name": "Kubernetes",
        "category": "orchestration",
        "icon": "☸️",
        "description": "Container orchestration platform for automating deployment, scaling, and management of containerized applications.",
        "supports": ["Auto-scaling (HPA, VPA)", "Service discovery", "Rolling updates", "Self-healing", "Config management", "Ingress"],
        "limitations": ["Steep learning curve", "Operational overhead", "Overkill for small teams", "YAML fatigue"],
        "when_to_use": ["10+ microservices", "Need auto-scaling and self-healing", "Multi-cloud deployment"],
        "when_not_to_use": ["Small projects with < 5 services → use Docker Compose", "Serverless workloads → use Lambda"],
        "interview_questions": ["Explain Kubernetes pod lifecycle.", "How does HPA work?", "What is a StatefulSet vs Deployment?"],
    },

    # ═══════════════════════════════════════════════
    # MONITORING
    # ═══════════════════════════════════════════════
    "prometheus": {
        "slug": "prometheus",
        "name": "Prometheus",
        "category": "monitoring",
        "icon": "📊",
        "description": "Open-source monitoring and alerting toolkit designed for reliability, using a pull-based metrics collection model.",
        "supports": ["Time-series metrics", "PromQL query language", "Alerting rules", "Service discovery", "Grafana integration"],
        "limitations": ["Not for logs or traces (use Loki/Jaeger)", "Single-node storage by default", "Pull-based (requires exposition)"],
        "when_to_use": ["Infrastructure monitoring", "Application metrics", "Alerting", "Kubernetes monitoring"],
        "when_not_to_use": ["Log aggregation → use ELK/Loki", "Distributed tracing → use Jaeger/Zipkin"],
        "interview_questions": ["Explain the four golden signals of monitoring.", "How does Prometheus service discovery work?"],
    },

    "grafana": {
        "slug": "grafana",
        "name": "Grafana",
        "category": "monitoring",
        "icon": "📈",
        "description": "Open-source observability platform for metrics visualization, dashboarding, and alerting.",
        "supports": ["Multi-datasource dashboards", "Alerting", "Annotations", "Templating", "Plugins"],
        "when_to_use": ["Visualizing Prometheus/InfluxDB/Elasticsearch metrics", "Operational dashboards"],
        "interview_questions": ["How would you design a monitoring stack for a microservices architecture?"],
    },
}
