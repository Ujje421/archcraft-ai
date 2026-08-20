# 04 — Architecture Overview

> The platform's own technical architecture — how all the pieces fit together.

---

## System Context

```mermaid
graph TB
    User["👤 User<br/>(Browser)"]
    Platform["🏗️ System Design Platform"]
    LLM["🤖 LLM Provider<br/>(OpenAI / Gemini)"]
    DB["🗄️ PostgreSQL + pgvector"]
    Cache["⚡ Redis"]
    
    User -->|"HTTPS"| Platform
    Platform -->|"API"| LLM
    Platform -->|"SQL"| DB
    Platform -->|"Cache"| Cache
```

---

## High-Level Architecture

```mermaid
graph TB
    subgraph Frontend["Frontend (React + TypeScript)"]
        Canvas["Architecture Canvas<br/>(React Flow)"]
        Designer["System Designer UI"]
        Assistant["AI Chat Panel"]
        Explorer["Component Explorer"]
        LevelSlider["Level Selector"]
    end

    subgraph API["API Layer"]
        Gateway["API Gateway<br/>(FastAPI Router)"]
    end

    subgraph Backend["Backend Engines (Python FastAPI)"]
        ArchEngine["Architecture Engine"]
        AIEngine["AI Engine"]
        CapEngine["Capacity Engine"]
        CostEngine["Cost Engine"]
        TradeEngine["Trade-off Engine"]
        ValidEngine["Validation Engine"]
    end

    subgraph Data["Data Layer"]
        PG["PostgreSQL<br/>+ pgvector"]
        Redis["Redis"]
        KB["Component<br/>Knowledge Base"]
    end

    subgraph External["External"]
        LLM["LLM Provider<br/>OpenAI / Gemini"]
    end

    Frontend -->|"REST / WebSocket"| Gateway
    Gateway --> ArchEngine
    Gateway --> AIEngine
    Gateway --> CapEngine
    Gateway --> CostEngine
    Gateway --> TradeEngine
    Gateway --> ValidEngine
    
    ArchEngine --> PG
    AIEngine --> LLM
    AIEngine --> KB
    AIEngine --> PG
    CapEngine --> Redis
    CostEngine --> Redis
    TradeEngine --> KB
    ValidEngine --> ArchEngine
    
    KB --> PG
```

---

## Layer Breakdown

### Layer 1: Frontend

| Component | Technology | Responsibility |
|---|---|---|
| Architecture Canvas | React Flow | Visual node/edge graph, drag-and-drop, zoom/pan |
| System Designer | React + TypeScript | Input form for new designs, parameter selection |
| AI Chat Panel | React | Chat interface for AI assistant |
| Component Explorer | React | Side panel with deep-dive component info |
| Level Selector | React | Slider/radio for Level 0–4 switching |
| State Management | Zustand | Global state: architecture graph, UI state, chat |
| API Client | Axios / fetch | REST communication with backend |
| WebSocket Client | Native WebSocket | Real-time AI streaming responses |

### Layer 2: API Gateway

| Component | Technology | Responsibility |
|---|---|---|
| API Router | FastAPI | Route requests to appropriate engine |
| Auth Middleware | FastAPI Depends | JWT validation, rate limiting |
| WebSocket Handler | FastAPI WebSocket | Stream AI responses |
| Request Validation | Pydantic | Validate all incoming requests |
| CORS | FastAPI CORS | Cross-origin resource sharing |

### Layer 3: Backend Engines

| Engine | Responsibility | Dependencies |
|---|---|---|
| **Architecture Engine** | Create, modify, validate architecture graphs | PostgreSQL, Validation Engine |
| **AI Engine** | Orchestrate LLM calls, structured output, RAG | LLM Provider, Knowledge Base, pgvector |
| **Capacity Engine** | Deterministic capacity calculations | None (pure computation) |
| **Cost Engine** | Infrastructure cost estimation | Cost data (static/Redis) |
| **Trade-off Engine** | Technology comparison and recommendation | Knowledge Base |
| **Validation Engine** | Validate architecture graph integrity | Architecture Engine |

### Layer 4: Data Layer

| Component | Technology | Stores |
|---|---|---|
| PostgreSQL | PostgreSQL 16+ | Systems, versions, nodes, connections, requirements, decisions |
| pgvector | pgvector extension | Embeddings for RAG (component knowledge, design patterns) |
| Redis | Redis 7+ | Session cache, rate limiting, capacity calc cache |
| Knowledge Base | PostgreSQL + JSON | Component metadata, comparison data, best practices |

---

## Data Flow: Generate a System Design

```mermaid
sequenceDiagram
    actor User
    participant UI as Frontend
    participant API as API Gateway
    participant Arch as Architecture Engine
    participant AI as AI Engine
    participant Cap as Capacity Engine
    participant LLM as LLM Provider
    participant DB as PostgreSQL

    User->>UI: "Design YouTube for 100M DAU"
    UI->>API: POST /api/v1/systems/generate
    API->>AI: Generate system design
    AI->>AI: Extract requirements from prompt
    AI->>Cap: Calculate capacity (100M DAU)
    Cap-->>AI: { rps: 57870, peak_rps: 289351, ... }
    AI->>LLM: Generate structured design (schema + capacity data)
    LLM-->>AI: { sections: [...], architecture_graph: {...} }
    AI->>AI: Validate and enrich response
    AI->>Arch: Store architecture graph
    Arch->>DB: INSERT system + nodes + connections
    Arch-->>API: { system_id, architecture_graph }
    API-->>UI: Complete design response
    UI->>UI: Render architecture on canvas
```

---

## Data Flow: AI Modifies Canvas

```mermaid
sequenceDiagram
    actor User
    participant UI as Frontend
    participant API as API Gateway
    participant AI as AI Engine
    participant Arch as Architecture Engine
    participant LLM as LLM Provider
    participant DB as PostgreSQL

    User->>UI: "Add Kafka for async processing"
    UI->>API: POST /api/v1/systems/{id}/ai/command
    Note over UI,API: Includes current architecture graph
    API->>AI: Process command with graph context
    AI->>LLM: "Given this architecture, add Kafka..."
    LLM-->>AI: { add_nodes: [...], add_connections: [...], explanation: "..." }
    AI->>Arch: Apply graph modifications
    Arch->>Arch: Validate new graph
    Arch->>DB: UPDATE nodes, connections (new version)
    Arch-->>API: { updated_graph, diff, explanation }
    API-->>UI: Graph diff + explanation
    UI->>UI: Animate canvas changes
```

---

## Communication Patterns

| Pattern | Used For | Protocol |
|---|---|---|
| REST | CRUD operations, design generation | HTTP/JSON |
| WebSocket | AI streaming responses, real-time collaboration | WS |
| Server-Sent Events | Long-running generation progress | SSE (alternative to WS) |

---

## Error Handling Strategy

```
Frontend
  → Retry with exponential backoff for transient errors
  → Show user-friendly error messages
  → Maintain canvas state even on API failure

API Gateway
  → Return structured error responses { error, code, message, details }
  → Rate limit per-user and per-endpoint
  → Circuit breaker for LLM provider

Backend Engines
  → Each engine handles its own errors
  → Fallback: if LLM fails, show cached/partial results
  → Validation engine catches invalid graph mutations

Data Layer
  → PostgreSQL transactions for graph mutations (all-or-nothing)
  → Redis fallback to PostgreSQL if cache is down
```

---

## Scalability Path

### MVP (Phase 1)
- Single FastAPI instance
- Single PostgreSQL instance
- Single Redis instance
- Direct LLM API calls

### Scale (Phase 2+)
- Multiple FastAPI workers behind load balancer
- PostgreSQL read replicas
- Redis cluster
- Background task queue (Celery/ARQ) for long-running generations
- LLM response caching

---

## Related Documents

- [05-frontend-architecture.md](./05-frontend-architecture.md) — Frontend deep dive
- [06-backend-architecture.md](./06-backend-architecture.md) — Backend engine details
- [07-ai-engine.md](./07-ai-engine.md) — AI pipeline
- [08-data-model.md](./08-data-model.md) — Database schema
