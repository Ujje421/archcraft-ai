# 17 — System Design Library

> Pre-built system designs across beginner → advanced difficulty.

---

## Overview

The library provides ready-made system designs that users can:

1. **Browse** — explore architectures for common systems
2. **Study** — understand how each system is designed at different levels
3. **Fork** — clone a design and modify it
4. **Practice** — use as interview prep material

---

## Library Categories

### 🟢 Beginner (5 systems)

Simple systems with 3-8 components. Focus on fundamentals.

| System | Domain | Key Concepts |
|---|---|---|
| **URL Shortener** | Web | Hashing, key-value store, redirect |
| **Pastebin** | Web | Object storage, expiration, unique IDs |
| **Todo App** | Web | CRUD, REST API, single database |
| **File Upload Service** | Storage | Object storage, metadata, chunked upload |
| **Chat Application** | Messaging | WebSocket, message queue, presence |

### 🟡 Intermediate (10 systems)

Production-grade systems with 10-20 components. Introduce caching, queues, and scaling.

| System | Domain | Key Concepts |
|---|---|---|
| **YouTube / Video Platform** | Media | CDN, transcoding, adaptive streaming, Kafka |
| **Netflix / Streaming** | Media | Recommendation, content delivery, microservices |
| **WhatsApp / Messenger** | Messaging | WebSocket, message delivery, E2E encryption |
| **Instagram / Photo Sharing** | Social | CDN, fan-out, feed generation, object storage |
| **Twitter / X** | Social | Fan-out on write vs read, timeline, trending |
| **Uber / Ride Sharing** | Transportation | Geolocation, matching, real-time tracking |
| **Food Delivery (DoorDash)** | E-commerce | Order management, driver matching, ETA |
| **E-commerce (Amazon)** | Commerce | Catalog, cart, checkout, inventory, payment |
| **Notification System** | Platform | Multi-channel (push, SMS, email), templating |
| **Rate Limiter** | Platform | Token bucket, sliding window, distributed |

### 🔴 Advanced (10 systems)

Large-scale distributed systems with 20-40 components. Deep technical challenges.

| System | Domain | Key Concepts |
|---|---|---|
| **Google Search** | Search | Web crawler, index, ranking, PageRank |
| **Distributed Database** | Data | Consensus, replication, sharding, transactions |
| **Payment System (Stripe)** | Financial | Idempotency, reconciliation, PCI, ledger |
| **Stock Trading Platform** | Financial | Low-latency, order matching, market data |
| **Notification Platform** | Platform | Multi-tenant, priority queues, deduplication |
| **Ad Platform (Google Ads)** | Advertising | Real-time bidding, click tracking, targeting |
| **Real-time Analytics** | Analytics | Stream processing, OLAP, data warehouse |
| **Recommendation System** | ML | Collaborative filtering, feature store, A/B test |
| **Ride Matching Engine** | Transportation | Geospatial indexing, optimization, supply-demand |
| **Distributed Job Scheduler** | Platform | DAG execution, retry, priority, resource mgmt |

---

## Library Entry Schema

Each pre-built system is stored as a complete system design:

```json
{
  "slug": "youtube",
  "name": "YouTube / Video Streaming Platform",
  "category": "intermediate",
  "difficulty": 3,                    // 1-5
  "domain": "media_streaming",
  "description": "A video streaming platform where users upload, transcode, and stream videos to millions of viewers.",
  "tags": ["video", "cdn", "transcoding", "streaming", "kafka"],
  
  "estimated_users": "500M total, 100M DAU",
  "key_challenges": [
    "Video transcoding at scale",
    "Global content delivery",
    "Real-time view counting",
    "Recommendation engine",
    "Copyright detection"
  ],
  
  "interview_frequency": "very_high",  // How often asked in interviews
  "companies": ["Google", "Netflix", "Meta", "Amazon"],
  
  "design": {
    "sections": { /* Full 26-section schema */ },
    "architecture": { /* Full graph: nodes + connections */ }
  },
  
  "levels": {
    "0": { "description": "Backend + Database", "node_count": 3 },
    "1": { "description": "+ LB, cache, replicas", "node_count": 6 },
    "2": { "description": "+ CDN, S3, Kafka, services", "node_count": 14 },
    "3": { "description": "+ Sharding, multi-region, observability", "node_count": 24 },
    "4": { "description": "Full production architecture", "node_count": 32 }
  }
}
```

---

## Library UI

```
┌──────────────────────────────────────────────────────────────┐
│ System Design Library                          🔍 Search    │
│                                                              │
│ Filter: [All] [Beginner] [Intermediate] [Advanced]          │
│ Sort:   [Popularity] [Difficulty] [Domain]                  │
│                                                              │
│ ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐│
│ │ 📹 YouTube       │ │ 🚗 Uber          │ │ 💬 WhatsApp      ││
│ │                  │ │                  │ │                  ││
│ │ Intermediate     │ │ Intermediate     │ │ Intermediate     ││
│ │ ⭐⭐⭐☆☆           │ │ ⭐⭐⭐⭐☆           │ │ ⭐⭐⭐☆☆           ││
│ │                  │ │                  │ │                  ││
│ │ CDN, Kafka,      │ │ Geolocation,     │ │ WebSocket,       ││
│ │ Transcoding      │ │ Matching         │ │ E2E Encryption   ││
│ │                  │ │                  │ │                  ││
│ │ 🏢 Google, Netflix│ │ 🏢 Uber, Lyft    │ │ 🏢 Meta, Signal  ││
│ │                  │ │                  │ │                  ││
│ │ [ View ] [ Fork ]│ │ [ View ] [ Fork ]│ │ [ View ] [ Fork ]││
│ └─────────────────┘ └─────────────────┘ └─────────────────┘│
│                                                              │
│ ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐│
│ │ 🔗 URL Shortener │ │ 🛒 E-commerce    │ │ 💳 Payment      ││
│ │                  │ │                  │ │                  ││
│ │ Beginner         │ │ Intermediate     │ │ Advanced         ││
│ │ ...              │ │ ...              │ │ ...              ││
│ └─────────────────┘ └─────────────────┘ └─────────────────┘│
└──────────────────────────────────────────────────────────────┘
```

---

## Fork Flow

When a user forks a library design:

1. Copy the complete design (graph + sections) into user's system list
2. User can modify everything
3. Original library design is unchanged
4. Fork history is tracked (for "based on" attribution)

```
Library: YouTube (read-only template)
  ↓ Fork
User: "My Video Platform" (fully editable copy)
  ↓ Modify
User: custom architecture with their changes
```

---

## Library API

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/v1/library` | List all designs (with filters) |
| GET | `/api/v1/library/{slug}` | Get full design |
| GET | `/api/v1/library/{slug}/preview` | Get summary only |
| POST | `/api/v1/library/{slug}/fork` | Fork into user's systems |

---

## Related Documents

- [14-interview-mode.md](./14-interview-mode.md) — Library designs used for interviews
- [02-system-design-schema.md](./02-system-design-schema.md) — Schema each design follows
- [09-component-knowledge-base.md](./09-component-knowledge-base.md) — Components used in designs
