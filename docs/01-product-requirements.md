# 01 — Product Requirements

---

## Functional Requirements

### MVP (Phase 1)

#### FR-1: System Design Generator

| ID | Requirement | Priority |
|---|---|---|
| FR-1.1 | User inputs a natural language problem statement (e.g., "Design YouTube") | P0 |
| FR-1.2 | User optionally specifies parameters: users, DAU, requests, availability, budget, regions | P0 |
| FR-1.3 | User selects experience level: Beginner / Intermediate / Advanced / Expert | P0 |
| FR-1.4 | User selects architecture style: Monolith / Modular Monolith / Microservices / Let AI Decide | P1 |
| FR-1.5 | Platform generates a complete structured design following the 26-section schema | P0 |
| FR-1.6 | Design output includes a structured architecture graph (JSON) | P0 |
| FR-1.7 | Design output renders on the interactive canvas | P0 |

#### FR-2: Interactive Architecture Canvas

| ID | Requirement | Priority |
|---|---|---|
| FR-2.1 | Canvas renders architecture as draggable nodes and connections | P0 |
| FR-2.2 | User can drag and reposition components | P0 |
| FR-2.3 | User can connect components with labeled edges | P0 |
| FR-2.4 | User can delete components and connections | P0 |
| FR-2.5 | User can duplicate components | P1 |
| FR-2.6 | User can group components into logical groups | P1 |
| FR-2.7 | User can add labels and notes to components | P1 |
| FR-2.8 | User can change the technology of any component | P0 |
| FR-2.9 | Canvas supports zoom, pan, and minimap | P0 |
| FR-2.10 | Canvas auto-layouts when generating architecture | P0 |
| FR-2.11 | Architecture is stored as structured JSON (not just visual) | P0 |

#### FR-3: AI Canvas Assistant

| ID | Requirement | Priority |
|---|---|---|
| FR-3.1 | User can ask questions about any component ("Why Redis?") | P0 |
| FR-3.2 | AI reads and understands the current canvas state | P0 |
| FR-3.3 | User can give AI modification commands ("Add Kafka for async processing") | P0 |
| FR-3.4 | AI automatically modifies the canvas (adds/removes/reconnects nodes) | P0 |
| FR-3.5 | AI can analyze the architecture against stated requirements | P0 |
| FR-3.6 | AI detects bottlenecks based on the actual architecture and capacity | P1 |
| FR-3.7 | AI suggests optimizations with "Apply recommended architecture" | P1 |

#### FR-4: Component Explorer

| ID | Requirement | Priority |
|---|---|---|
| FR-4.1 | Clicking any component opens a detail panel | P0 |
| FR-4.2 | Panel shows: why used, what it solves, alternatives, when NOT to use | P0 |
| FR-4.3 | Panel shows: partition/replication strategy (where applicable) | P1 |
| FR-4.4 | Panel shows: failure scenarios and recovery | P1 |
| FR-4.5 | Panel shows: expected throughput and scaling strategy | P1 |
| FR-4.6 | Panel shows: cost implications | P2 |
| FR-4.7 | Panel shows: production configuration recommendations | P2 |
| FR-4.8 | Panel shows: common interview questions about this component | P1 |

#### FR-5: Design Levels (Beginner → Expert)

| ID | Requirement | Priority |
|---|---|---|
| FR-5.1 | Every system design supports Level 0–4 complexity modes | P0 |
| FR-5.2 | Level 0 (Beginner): User → Backend → Database, simple language | P0 |
| FR-5.3 | Level 1 (Basic Production): + Load Balancer, API Servers, Cache | P0 |
| FR-5.4 | Level 2 (Intermediate): + CDN, Redis, MQ, Object Storage, Read Replicas, Monitoring | P0 |
| FR-5.5 | Level 3 (Advanced): + Kafka, Sharding, Multi-region, Circuit Breakers, Observability | P0 |
| FR-5.6 | Level 4 (Principal/Staff): Platform asks challenge questions (RPO/RTO, failure, spikes) | P1 |
| FR-5.7 | Switching levels transforms the architecture on the canvas | P0 |

---

### V2 (Phase 2)

#### FR-6: Capacity Estimation Engine

| ID | Requirement | Priority |
|---|---|---|
| FR-6.1 | Deterministic calculation engine (not LLM arithmetic) | P0 |
| FR-6.2 | Calculates: total requests/day, avg RPS, peak RPS, storage, bandwidth | P0 |
| FR-6.3 | Recommends infrastructure sizing based on calculations | P0 |
| FR-6.4 | Updates when user changes parameters | P0 |

#### FR-7: Cost Estimation Engine

| ID | Requirement | Priority |
|---|---|---|
| FR-7.1 | Estimates monthly infrastructure cost per component | P0 |
| FR-7.2 | Recalculates when architecture or user count changes | P0 |
| FR-7.3 | AI can suggest cost optimization strategies | P1 |
| FR-7.4 | Shows savings percentage for optimized architecture | P1 |

#### FR-8: Trade-off Engine

| ID | Requirement | Priority |
|---|---|---|
| FR-8.1 | Compare two technologies side-by-side (e.g., PostgreSQL vs DynamoDB) | P0 |
| FR-8.2 | Generate comparison matrix with star ratings | P0 |
| FR-8.3 | Provide recommendation based on system requirements | P0 |
| FR-8.4 | "Challenge this decision" — AI argues the opposite side | P1 |

#### FR-9: Failure Simulation (Chaos Mode)

| ID | Requirement | Priority |
|---|---|---|
| FR-9.1 | Randomly break a component in the architecture | P0 |
| FR-9.2 | Show impact: affected users, RTO, RPO | P0 |
| FR-9.3 | Show recommended recovery steps | P0 |
| FR-9.4 | "Fix Architecture" — AI suggests resilience improvements | P1 |

#### FR-10: Architecture Comparison & Diff

| ID | Requirement | Priority |
|---|---|---|
| FR-10.1 | Compare two architecture versions side-by-side | P0 |
| FR-10.2 | Show diff table: complexity, scalability, availability, cost, operations, throughput | P0 |
| FR-10.3 | Explain why the architecture changed | P0 |

#### FR-11: Version History

| ID | Requirement | Priority |
|---|---|---|
| FR-11.1 | Every architecture modification creates a new version | P0 |
| FR-11.2 | User can browse and restore previous versions | P0 |
| FR-11.3 | Diff view between any two versions | P1 |

#### FR-12: Interview Mode

| ID | Requirement | Priority |
|---|---|---|
| FR-12.1 | User selects: system, difficulty, duration, interviewer strictness | P0 |
| FR-12.2 | AI acts as interviewer, asks progressive questions | P0 |
| FR-12.3 | Evaluates user's answers in real-time | P0 |
| FR-12.4 | Final score across 7+ dimensions | P0 |

---

### V3 (Phase 3)

#### FR-13: Learning Platform

| ID | Requirement | Priority |
|---|---|---|
| FR-13.1 | Structured courses on system design topics | P0 |
| FR-13.2 | Interactive problems with AI evaluation | P0 |

#### FR-14: AI Architecture Review

| ID | Requirement | Priority |
|---|---|---|
| FR-14.1 | AI reviews user-designed architecture and provides score | P0 |
| FR-14.2 | Identifies weaknesses, bottlenecks, single points of failure | P0 |

#### FR-15: Engineering Mode

| ID | Requirement | Priority |
|---|---|---|
| FR-15.1 | Generate API specifications from architecture | P0 |
| FR-15.2 | Generate Terraform/IaC from architecture | P1 |
| FR-15.3 | Generate Kubernetes YAML from architecture | P1 |

---

## Non-Functional Requirements

| ID | Requirement | Target |
|---|---|---|
| NFR-1 | Design generation latency | < 30 seconds |
| NFR-2 | AI response latency | < 3 seconds |
| NFR-3 | Canvas interaction latency | < 200ms (60fps) |
| NFR-4 | Concurrent users | 100+ (MVP) |
| NFR-5 | Architecture graph size | Up to 200 nodes per design |
| NFR-6 | Browser support | Chrome, Firefox, Safari, Edge (latest) |
| NFR-7 | Mobile responsiveness | View-only on mobile, full editing on desktop |
| NFR-8 | Data persistence | All designs saved to PostgreSQL |
| NFR-9 | API response format | JSON, structured, consistent |
| NFR-10 | Availability | 99.9% (MVP) |

---

## Related Documents

- [00-product-vision.md](./00-product-vision.md) — Product vision
- [02-system-design-schema.md](./02-system-design-schema.md) — Schema that structures every design
- [04-architecture-overview.md](./04-architecture-overview.md) — Platform architecture
