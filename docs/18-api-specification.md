# 18 — API Specification

> Complete REST API specification for the platform.

---

## Base URL

```
Development: http://localhost:8000/api/v1
Production:  https://api.systemdesign.ai/api/v1
```

## Authentication

```
Authorization: Bearer <jwt_token>
```

MVP: Optional (single-user mode)
V2: Required (Google OAuth + JWT)

## Response Format

All responses follow:

```json
{
  "success": true,
  "data": { ... },
  "error": null
}

// Error:
{
  "success": false,
  "data": null,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid architecture: node 'redis' has no connections",
    "details": { ... }
  }
}
```

---

## Systems

### Create System (Generate)

```
POST /systems/generate

Request:
{
  "prompt": "Design a food delivery platform",
  "parameters": {
    "total_users": 10000000,
    "dau": 3000000,
    "requests_per_user_per_day": 50,
    "availability": "99.99",
    "regions": "multi-region",
    "budget_monthly": 20000
  },
  "level": 2,
  "architecture_style": "microservices"  // optional: monolith, modular_monolith, microservices, auto
}

Response: 201 Created
{
  "success": true,
  "data": {
    "id": "uuid",
    "title": "Food Delivery Platform",
    "description": "...",
    "domain": "food_delivery",
    "active_level": 2,
    "current_version": 1,
    "architecture": {
      "nodes": [...],
      "connections": [...]
    },
    "sections": {
      "problem_definition": {...},
      "functional_requirements": {...},
      // ... all 26 sections
    },
    "capacity": {...},
    "created_at": "2024-01-15T12:00:00Z"
  }
}
```

### List Systems

```
GET /systems?page=1&limit=20&domain=food_delivery

Response: 200 OK
{
  "data": {
    "items": [...],
    "total": 42,
    "page": 1,
    "pages": 3
  }
}
```

### Get System

```
GET /systems/{id}?level=3

Response: 200 OK
{
  "data": {
    "id": "uuid",
    "title": "...",
    "architecture": {
      "nodes": [...],          // Filtered by level
      "connections": [...]     // Filtered by level
    },
    "sections": {...}
  }
}
```

### Update System

```
PUT /systems/{id}

Request:
{
  "title": "Updated title",
  "active_level": 3,
  "parameters": {...}
}
```

### Delete System

```
DELETE /systems/{id}

Response: 204 No Content
```

---

## Graph Manipulation

### Add Node

```
POST /systems/{id}/nodes

Request:
{
  "node_id": "redis_cache",
  "type": "cache",
  "technology": "Redis",
  "label": "Session Cache",
  "min_level": 2,
  "position": { "x": 400, "y": 300 },
  "metadata": { "cluster_mode": true, "nodes": 3 }
}

Response: 201 Created
{
  "data": {
    "id": "uuid",
    "node_id": "redis_cache",
    "version": 2
  }
}
```

### Update Node

```
PUT /systems/{id}/nodes/{node_id}

Request:
{
  "technology": "Memcached",
  "label": "Memcached Cache",
  "position": { "x": 410, "y": 310 },
  "metadata": { "cluster_mode": false }
}
```

### Delete Node

```
DELETE /systems/{id}/nodes/{node_id}

Response: 200 OK
{
  "data": {
    "removed_node": "redis_cache",
    "removed_connections": ["api_to_redis", "redis_to_db"],
    "version": 3
  }
}
```

### Add Connection

```
POST /systems/{id}/connections

Request:
{
  "source_node_id": "api_service",
  "target_node_id": "redis_cache",
  "label": "Cache lookup",
  "protocol": "TCP",
  "min_level": 2
}
```

### Delete Connection

```
DELETE /systems/{id}/connections/{connection_id}
```

---

## AI Assistant

### Send Command

```
POST /systems/{id}/ai/command

Request:
{
  "command": "Add Kafka for async order processing",
  "current_graph": {              // Optional: send current graph state
    "nodes": [...],
    "connections": [...]
  }
}

Response: 200 OK
{
  "data": {
    "diff": {
      "add_nodes": [
        {
          "node_id": "kafka",
          "type": "message_queue",
          "technology": "Apache Kafka",
          "label": "Event Bus",
          "min_level": 3,
          "metadata": { "partitions": 12 }
        }
      ],
      "remove_nodes": [],
      "add_connections": [
        {
          "source_node_id": "order_service",
          "target_node_id": "kafka",
          "label": "Order events",
          "protocol": "async"
        },
        {
          "source_node_id": "kafka",
          "target_node_id": "notification_service",
          "label": "Process events",
          "protocol": "async"
        }
      ],
      "remove_connections": []
    },
    "explanation": "Added Kafka as an event bus between Order Service and downstream consumers. This decouples order processing from notification delivery and analytics, allowing each to scale independently.",
    "warnings": [],
    "new_version": 4
  }
}
```

### Explain Component

```
POST /systems/{id}/ai/explain

Request:
{
  "node_id": "kafka",
  "question": "Why Kafka instead of RabbitMQ?"  // Optional
}

Response: 200 OK
{
  "data": {
    "component": "Apache Kafka",
    "why_used": "Kafka was chosen for async order processing because...",
    "problem_solved": "Decouples order creation from downstream processing...",
    "alternatives": [
      {
        "technology": "RabbitMQ",
        "why_not": "Lower throughput, no event replay capability"
      },
      {
        "technology": "Amazon SQS",
        "why_not": "Limited ordering guarantees at scale"
      }
    ],
    "when_not_to_use": ["Simple task queues with low volume", "..."],
    "failure_scenarios": [...],
    "scaling_strategy": "...",
    "cost_implications": "...",
    "interview_questions": [...]
  }
}
```

### Analyze Bottlenecks

```
POST /systems/{id}/ai/analyze

Request:
{
  "analysis_type": "bottlenecks",    // bottlenecks, spof, cost, latency
  "target_rps": 1000000              // Optional: analyze for specific load
}

Response: 200 OK
{
  "data": {
    "issues": [
      {
        "severity": "critical",
        "component": "postgresql",
        "issue": "Single database cannot handle 1M RPS",
        "current_capacity": "~50K writes/sec",
        "required_capacity": "100K writes/sec",
        "recommendations": [
          "Add Redis cache layer (reduces DB load by ~80%)",
          "Add read replicas (handles read scaling)",
          "Implement database sharding (for write scaling)",
          "Introduce Kafka for async writes"
        ]
      }
    ],
    "suggested_diff": { ... }  // GraphDiff to fix issues
  }
}
```

### AI Chat (WebSocket)

```
WS /ws/systems/{id}/ai/chat

Client → Server:
{
  "type": "message",
  "content": "How would this handle a Black Friday traffic spike?"
}

Server → Client (streaming):
{
  "type": "chunk",
  "content": "During a Black Friday..."
}
{
  "type": "chunk",
  "content": "traffic spike, several components..."
}
{
  "type": "complete",
  "content": "full response text",
  "suggested_actions": ["Scale to 10M users", "Add CDN"]
}
```

---

## Engines

### Capacity Calculation

```
POST /capacity/calculate

Request:
{
  "total_users": 100000000,
  "dau": 30000000,
  "requests_per_user_per_day": 50,
  "read_write_ratio": 10,
  "avg_request_payload_kb": 5,
  "avg_object_size_mb": 1,
  "peak_multiplier": 5
}

Response: 200 OK
{
  "data": {
    "total_requests_per_day": 1500000000,
    "average_rps": 17361.11,
    "peak_rps": 86805.56,
    "read_rps": 15783.73,
    "write_rps": 1577.37,
    "daily_data_ingestion_gb": 7.15,
    "monthly_storage_gb": 214.58,
    "yearly_storage_tb": 2.57,
    "cache_size_gb": 1.43,
    "recommendations": {
      "api_instances_min": 44,
      "api_instances_max": 88,
      "database_type": "sharded",
      "database_replicas": 9,
      "cache_needed": true,
      "queue_needed": true,
      "cdn_needed": true
    },
    "formulas": [
      {
        "name": "Average RPS",
        "formula": "1,500,000,000 / 86,400",
        "result": "17,361 RPS"
      }
    ]
  }
}
```

### Cost Estimation

```
POST /cost/estimate

Request:
{
  "system_id": "uuid",        // Uses system's graph + capacity
  "cloud_provider": "aws",
  "reserved_instances": false
}

Response: 200 OK
{
  "data": {
    "total_monthly": 12100.00,
    "currency": "USD",
    "breakdown": [
      { "node_id": "api_servers", "component": "FastAPI", "category": "compute", "monthly_cost": 4200 },
      { "node_id": "postgres", "component": "PostgreSQL", "category": "database", "monthly_cost": 3100 },
      { "node_id": "redis", "component": "Redis", "category": "cache", "monthly_cost": 800 }
    ],
    "by_category": {
      "compute": 4200,
      "database": 3100,
      "cache": 800,
      "messaging": 1200,
      "storage": 900,
      "cdn": 1400,
      "monitoring": 500
    }
  }
}
```

### Technology Comparison

```
POST /tradeoffs/compare

Request:
{
  "tech_a": "postgresql",
  "tech_b": "dynamodb",
  "requirements": ["relational_data", "complex_queries", "acid_transactions", "horizontal_scaling"]
}

Response: 200 OK
{
  "data": {
    "criteria": [
      { "name": "Relational data", "score_a": 5, "score_b": 1, "weight": 0.9 },
      { "name": "Complex queries", "score_a": 5, "score_b": 2, "weight": 0.8 }
    ],
    "recommendation": {
      "recommended": "postgresql",
      "confidence": 0.82,
      "reasoning": "..."
    }
  }
}
```

---

## Knowledge Base

### List Components

```
GET /components?category=database

Response: 200 OK
{
  "data": [
    {
      "slug": "postgresql",
      "name": "PostgreSQL",
      "category": "database",
      "icon": "🐘",
      "description": "Open-source relational database..."
    }
  ]
}
```

### Get Component Detail

```
GET /components/postgresql

Response: 200 OK
{
  "data": {
    "slug": "postgresql",
    "name": "PostgreSQL",
    "category": "database",
    "description": "...",
    "supports": [...],
    "limitations": [...],
    "when_to_use": [...],
    "when_not_to_use": [...],
    "scaling": {...},
    "failure_modes": [...],
    "cost_model": {...},
    "interview_questions": [...],
    "production_config": {...}
  }
}
```

---

## Export

```
POST /systems/{id}/export

Request:
{
  "format": "markdown",
  "level": 3,
  "include_sections": true
}

Response: 200 OK
{
  "data": {
    "format": "markdown",
    "filename": "food_delivery_system_design.md",
    "content": "# Food Delivery Platform..."
  }
}
```

---

## Library

```
GET /library?category=intermediate&sort=popularity

POST /library/{slug}/fork

Response: 201 Created
{
  "data": {
    "system_id": "uuid",
    "forked_from": "youtube",
    "message": "System forked successfully"
  }
}
```

---

## Rate Limits

| Endpoint | Limit |
|---|---|
| `/systems/generate` | 10/hour |
| `/ai/*` | 60/hour |
| `/capacity/*` | 100/hour |
| All other endpoints | 1000/hour |

---

## Related Documents

- [06-backend-architecture.md](./06-backend-architecture.md) — Backend implementation
- [05-frontend-architecture.md](./05-frontend-architecture.md) — Frontend API client
