# ⚡ ArchCraft (`archcraft-ai`)

> **AI-native system architecture platform for designing, understanding, evaluating, and evolving software systems.**

Design systems. Understand trade-offs. Simulate failure. Build better architectures.

[![GitHub Repo](https://img.shields.io/badge/GitHub-Ujje421%2Farchcraft--ai-181717?logo=github)](https://github.com/Ujje421/archcraft-ai)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688.svg?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/Frontend-React%20%2B%20TS-61DAFB.svg?logo=react&logoColor=black)](https://react.dev)
[![React Flow](https://img.shields.io/badge/Canvas-React%20Flow-FF0072.svg)](https://reactflow.dev)
[![PostgreSQL](https://img.shields.io/badge/Database-PostgreSQL%20%2B%20pgvector-336791.svg?logo=postgresql&logoColor=white)](https://www.postgresql.org)

---

## What Is This?

An AI-powered platform where you go from:

**Problem → Requirements → Architecture → Components → Data Model → APIs → Scalability → Security → Failure Handling → Cost → Architecture Diagram → Interview Discussion → Production Design**

Think of it as: **Figma + Excalidraw + ChatGPT + System Design Interviewer + Architecture Knowledge Base**

---

## Core Features (MVP)

| Feature | Description |
|---|---|
| 🏗️ **System Design Generator** | Input "Design YouTube" → get a complete structured design |
| 🎨 **Interactive Architecture Canvas** | Visual canvas with draggable, connectable, clickable components |
| 🤖 **AI Canvas Assistant** | Ask "Why Redis?" or say "Add Kafka" — AI understands and modifies the canvas |
| 🔍 **Component Explorer** | Click any component → deep dive on why, scaling, failures, cost, alternatives |
| 📊 **Beginner → Expert Mode** | Same system at 5 complexity levels (Level 0–4) |

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React + TypeScript + React Flow + Tailwind CSS |
| Backend | Python FastAPI |
| Database | PostgreSQL + pgvector |
| Cache | Redis |
| AI | OpenAI / Gemini (structured JSON output + RAG) |

---

## Architecture Documentation

All architecture documents are in the [`docs/`](./docs/) directory:

| # | Document | Description |
|---|---|---|
| 00 | [Product Vision](./docs/00-product-vision.md) | Why we're building this |
| 01 | [Product Requirements](./docs/01-product-requirements.md) | What we're building (functional + non-functional) |
| 02 | [System Design Schema](./docs/02-system-design-schema.md) | The 26-section standardized schema |
| 03 | [Design Levels](./docs/03-design-levels.md) | Level 0–4 complexity progression |
| 04 | [Architecture Overview](./docs/04-architecture-overview.md) | Platform's own architecture |
| 05 | [Frontend Architecture](./docs/05-frontend-architecture.md) | React + React Flow canvas |
| 06 | [Backend Architecture](./docs/06-backend-architecture.md) | FastAPI engines and services |
| 07 | [AI Engine](./docs/07-ai-engine.md) | Multi-step AI pipeline |
| 08 | [Data Model](./docs/08-data-model.md) | PostgreSQL schema |
| 09 | [Component Knowledge Base](./docs/09-component-knowledge-base.md) | 49+ infrastructure components |
| 10 | [Capacity Engine](./docs/10-capacity-engine.md) | Deterministic capacity calculation |
| 11 | [Cost Engine](./docs/11-cost-engine.md) | Infrastructure cost estimation |
| 12 | [Trade-off Engine](./docs/12-tradeoff-engine.md) | Technology comparison |
| 13 | [Canvas Architecture](./docs/13-canvas-architecture.md) | Interactive canvas spec |
| 14 | [Interview Mode](./docs/14-interview-mode.md) | AI interview simulator |
| 15 | [Failure Simulation](./docs/15-failure-simulation.md) | Chaos mode |
| 16 | [Export System](./docs/16-export-system.md) | PNG/SVG/JSON/MD/Terraform |
| 17 | [System Design Library](./docs/17-system-design-library.md) | 25 pre-built designs |
| 18 | [API Specification](./docs/18-api-specification.md) | Complete REST API spec |
| 19 | [Deployment](./docs/19-deployment.md) | Infrastructure & CI/CD |
| 20 | [Roadmap](./docs/20-roadmap.md) | MVP → V2 → V3 timeline |

---

## Quick Start

```bash
# Clone
git clone https://github.com/Ujje421/archcraft-ai.git
cd archcraft-ai

# Backend
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env  # Add your LLM API key
alembic upgrade head
uvicorn app.main:app --reload

# Frontend (new terminal)
cd frontend
npm install
npm run dev
```

Or with Docker:

```bash
docker compose up
```

---

## Key Design Decisions

1. **The LLM is NOT the source of truth.** The structured architecture graph is.
2. **Real computation, not LLM arithmetic.** Capacity and cost use deterministic engines.
3. **Every decision is explainable.** Click anything → understand why.
4. **26-section schema.** Every design is consistent, comparable, and controllable.
5. **5 complexity levels.** Same system, different depths — beginner to principal engineer.

---

## Roadmap

- **MVP** — Generator, Canvas, AI Assistant, Explorer, Levels
- **V2** — Cost Engine, Interview Mode, Chaos Mode, Version History
- **V3** — Learning Platform, Terraform Export, Multi-Agent AI, Collaboration

---

## License

MIT
