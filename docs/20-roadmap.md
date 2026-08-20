# 20 — Roadmap

> Phased roadmap from MVP to V3.

---

## Timeline Overview

```mermaid
gantt
    title System Design Platform Roadmap
    dateFormat  YYYY-MM-DD
    
    section Phase 1: MVP
    Documentation & Architecture    :done, doc, 2024-01-01, 2024-01-14
    Backend: Core Engines           :active, be1, 2024-01-15, 2024-02-15
    Backend: AI Engine              :ai1, 2024-02-01, 2024-02-28
    Frontend: Canvas                :fe1, 2024-02-01, 2024-03-15
    Frontend: UI Components         :fe2, 2024-02-15, 2024-03-15
    Knowledge Base Seeding          :kb1, 2024-03-01, 2024-03-15
    Integration & Testing           :int1, 2024-03-15, 2024-03-31
    
    section Phase 2: V2
    Capacity & Cost Engines         :ce1, 2024-04-01, 2024-04-30
    Trade-off Engine                :te1, 2024-04-15, 2024-05-15
    Interview Mode                  :iv1, 2024-05-01, 2024-05-31
    Failure Simulation              :fs1, 2024-05-15, 2024-06-15
    Version History & Diff          :vh1, 2024-06-01, 2024-06-30
    
    section Phase 3: V3
    Learning Platform               :lp1, 2024-07-01, 2024-08-31
    Engineering Mode                :em1, 2024-09-01, 2024-10-31
    Multi-Agent Architecture        :ma1, 2024-11-01, 2024-12-31
```

---

## Phase 1: MVP

**Duration**: ~3 months
**Goal**: Core platform with 5 killer features

### Sprint 1-2: Foundation (Weeks 1-4)

| Task | Priority | Effort |
|---|---|---|
| Project scaffolding (Vite + FastAPI) | P0 | 2 days |
| PostgreSQL schema + migrations | P0 | 3 days |
| Pydantic schemas (all request/response models) | P0 | 3 days |
| FastAPI router + dependency injection | P0 | 2 days |
| Capacity Engine (full implementation + tests) | P0 | 3 days |
| Validation Engine (basic graph checks) | P0 | 2 days |
| Architecture Engine (CRUD operations) | P0 | 3 days |
| Component Knowledge Base loader + 20 components | P0 | 5 days |
| React project setup + Tailwind + routing | P0 | 2 days |
| Design system (tokens, base components) | P0 | 3 days |

**Milestone**: Backend serves capacity calculations, component knowledge. Frontend renders basic UI.

### Sprint 3-4: AI + Canvas (Weeks 5-8)

| Task | Priority | Effort |
|---|---|---|
| LLM provider abstraction (OpenAI + Gemini) | P0 | 3 days |
| Structured output schema enforcement | P0 | 3 days |
| AI design generation pipeline | P0 | 5 days |
| System prompts (generate, modify, explain) | P0 | 3 days |
| RAG pipeline (pgvector embeddings) | P1 | 3 days |
| React Flow canvas integration | P0 | 5 days |
| Custom node components (10 types) | P0 | 5 days |
| Component palette (drag-and-drop) | P0 | 3 days |
| Auto-layout (dagre) | P0 | 2 days |

**Milestone**: User can input "Design YouTube" and see architecture on canvas.

### Sprint 5-6: Features + Polish (Weeks 9-12)

| Task | Priority | Effort |
|---|---|---|
| AI Canvas Assistant (chat panel) | P0 | 5 days |
| AI command processing (add/remove/modify) | P0 | 5 days |
| Component Explorer panel | P0 | 5 days |
| Level selector (0-4) with canvas filtering | P0 | 3 days |
| Level transition animations | P1 | 2 days |
| System Design Generator page (form UI) | P0 | 3 days |
| Schema section panels (tabs) | P0 | 5 days |
| Export (JSON, Markdown, PNG) | P0 | 3 days |
| System list / dashboard page | P0 | 3 days |
| Library page (5 pre-built designs) | P1 | 3 days |
| WebSocket streaming for AI responses | P1 | 3 days |
| Error handling + loading states | P0 | 2 days |
| Responsive layout | P1 | 2 days |
| E2E testing | P1 | 3 days |

**Milestone**: Complete MVP — all 5 core features working.

### MVP Deliverables

- [x] System Design Generator
- [x] Interactive Architecture Canvas (React Flow)
- [x] AI Canvas Assistant (chat + commands)
- [x] Component Explorer (click → deep dive)
- [x] Beginner → Expert mode (Level 0-4)
- [x] 50+ components in knowledge base
- [x] 5 pre-built system designs
- [x] Export: JSON, Markdown, PNG
- [x] Capacity Engine (deterministic)

---

## Phase 2: V2

**Duration**: ~3 months
**Goal**: Advanced features — engines, interview, simulation

### V2 Features

| Feature | Effort | Key Components |
|---|---|---|
| **Cost Estimation Engine** | 2 weeks | Cloud pricing data, per-component cost, optimization |
| **Trade-off Engine** | 2 weeks | Comparison matrix, scoring, challenge mode |
| **Architecture Diff** | 1 week | Version comparison, diff table, explanation |
| **Version History** | 1 week | Snapshot, restore, browse versions |
| **Interview Mode** | 3 weeks | AI interviewer, scoring rubric, feedback report |
| **Failure Simulation** | 2 weeks | Chaos mode, impact analysis, recovery steps |
| **PDF Export** | 1 week | Professional design document |
| **Additional Library Designs** | 2 weeks | 20 more pre-built designs |
| **User Authentication** | 1 week | Google OAuth, JWT, user profiles |

### V2 Deliverables

- [ ] Cost Estimation Engine
- [ ] Trade-off Engine + Challenge Mode
- [ ] Architecture Diff + Version History
- [ ] Interview Mode with scoring
- [ ] Failure Simulation (Chaos Mode)
- [ ] PDF export
- [ ] 25 pre-built system designs
- [ ] User authentication

---

## Phase 3: V3

**Duration**: ~6 months
**Goal**: Full platform — learning, engineering, deployment

### V3 Features

| Feature | Effort | Description |
|---|---|---|
| **Learning Platform** | 4 weeks | Structured courses, interactive problems |
| **AI Architecture Review** | 2 weeks | Score user-designed architectures |
| **Multi-Agent Architecture** | 4 weeks | Specialized agents (DB, scaling, security, cost) |
| **API Spec Generation** | 2 weeks | OpenAPI/Swagger from architecture |
| **Terraform Export** | 3 weeks | Generate IaC from architecture |
| **Kubernetes YAML Export** | 2 weeks | Generate K8s manifests |
| **Collaboration** | 4 weeks | Multi-user, real-time editing |
| **Template Marketplace** | 2 weeks | Community-shared designs |
| **Custom Components** | 2 weeks | Users create their own components |

### V3 Deliverables

- [ ] Learning platform with courses
- [ ] AI Architecture Review + scoring
- [ ] Multi-agent AI architecture
- [ ] Engineering Mode (API spec, Terraform, K8s)
- [ ] Real-time collaboration
- [ ] Template marketplace
- [ ] Custom component creation

---

## Success Criteria

### MVP Success

| Metric | Target |
|---|---|
| Can generate complete design from prompt | ✓ |
| Canvas renders with 20+ nodes smoothly | ✓ |
| AI modifies canvas from natural language | ✓ |
| Level switching works with animation | ✓ |
| Component explorer shows deep information | ✓ |
| Capacity Engine produces correct numbers | 100% test pass |
| Export works in 3+ formats | ✓ |
| Page load time | < 3 seconds |
| Design generation time | < 30 seconds |

### V2 Success

| Metric | Target |
|---|---|
| Interview mode produces useful feedback | User satisfaction > 4/5 |
| Cost estimation within 20% of real costs | ✓ |
| Failure simulation shows meaningful insights | ✓ |
| 25+ pre-built designs available | ✓ |

### V3 Success

| Metric | Target |
|---|---|
| Terraform output is valid and deployable | ✓ |
| Multi-agent produces better designs than single | A/B tested |
| Collaboration works with 5+ concurrent users | ✓ |

---

## Related Documents

- [00-product-vision.md](./00-product-vision.md) — What we're building and why
- [01-product-requirements.md](./01-product-requirements.md) — Detailed requirements
- [04-architecture-overview.md](./04-architecture-overview.md) — Technical architecture
