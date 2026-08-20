# 00 — Product Vision

> **AI-native system architecture platform for designing, understanding, evaluating, and evolving software systems.**

---

## One-Liner

**Design systems. Understand trade-offs. Build better architectures.**

---

## The Problem

System design is one of the most complex skills in software engineering, yet the tools available are:

| Current Tool | Limitation |
|---|---|
| Whiteboards | No intelligence, no validation, no persistence |
| Excalidraw / draw.io | Visual only — no understanding of what's drawn |
| ChatGPT / Gemini | Text-only, no visual, no structured output, hallucinated numbers |
| System design courses | Static content, no interactivity, no personalization |
| Interview prep sites | Flashcard-style, no real architecture building |

**No tool combines visual architecture building with AI-powered reasoning.**

---

## The Solution

An AI-powered platform where users go from:

```
Problem → Requirements → Architecture → Components → Data Model → APIs
→ Scalability → Security → Failure Handling → Cost → Architecture Diagram
→ Interview Discussion → Production Design
```

The platform is:

```
Figma          → Visual canvas for architecture
Excalidraw     → Free-form drawing and arrangement
ChatGPT        → AI reasoning about every decision
Interviewer    → Practice system design interviews
Knowledge Base → Deep library of infrastructure components
```

---

## Core Principles

### 1. Structured, Not Random

Every system design follows a **26-section standardized schema** (see [02-system-design-schema.md](./02-system-design-schema.md)). The AI fills the schema — it doesn't free-form generate.

### 2. The Graph Is the Source of Truth

The architecture is stored as a **structured JSON graph** of nodes and connections. The LLM reads, reasons about, and modifies this graph. The LLM is never the source of truth.

```json
{
  "nodes": [
    { "id": "api_gateway", "type": "api_gateway", "technology": "Kong" },
    { "id": "order_service", "type": "service", "technology": "FastAPI" }
  ],
  "connections": [
    { "source": "api_gateway", "target": "order_service", "protocol": "HTTPS" }
  ]
}
```

### 3. Real Computation, Not Hallucination

Capacity estimation, cost calculation, and throughput analysis use **deterministic computation engines**, not LLM arithmetic.

### 4. Multiple Depths

Every system design has **5 complexity levels** (Level 0–4). A beginner and a staff engineer see the same system at different depths.

### 5. Every Decision Is Explainable

Click any component or connection → the platform explains **why** it exists, what alternatives were considered, and what trade-offs were made.

---

## Target Audience

| Audience | Use Case |
|---|---|
| **Junior Engineers** | Learn system design from scratch with progressive complexity |
| **Mid-level Engineers** | Understand trade-offs, build real production architectures |
| **Senior/Staff Engineers** | Evaluate architectures, simulate failures, estimate costs |
| **Engineering Managers** | Review and validate team architecture decisions |
| **Interview Candidates** | Practice system design interviews with AI interviewer |
| **Interviewers** | Generate structured evaluation criteria |
| **Startups** | Quickly design and evaluate architecture options |
| **Consultants** | Generate architecture documentation and recommendations |

---

## Product Positioning

### What We Are

> An AI-native system architecture platform for designing, understanding, evaluating, and evolving software systems.

### What We Are NOT

- Not a simple "ChatGPT system design generator"
- Not a static diagramming tool
- Not a course platform with pre-recorded videos
- Not an infrastructure-as-code tool (though we can export to IaC)

---

## Competitive Landscape

| Competitor | Strength | Our Advantage |
|---|---|---|
| Excalidraw | Beautiful drawing | Our canvas understands what's drawn |
| ChatGPT | Flexible AI | Structured output + visual canvas + real computation |
| HelloInterview | Interview prep | Full architecture platform, not just interview Q&A |
| Lucidchart | Professional diagrams | AI-powered, interactive, intelligent components |
| draw.io | Free diagrams | Every component is interactive and explainable |

---

## Success Metrics (MVP)

| Metric | Target |
|---|---|
| Time to generate complete design | < 30 seconds |
| Design sections covered | 26/26 schema sections |
| Canvas interaction latency | < 200ms |
| AI response time | < 3 seconds |
| Component knowledge base | 50+ components |
| Pre-built system designs | 20+ |

---

## Platform Name Candidates

(To be decided)

- ArchFlow
- SystemForge
- DesignEngine
- ArchitectAI
- SysDesigner
- Blueprint AI

---

## Related Documents

- [01-product-requirements.md](./01-product-requirements.md) — Detailed requirements
- [02-system-design-schema.md](./02-system-design-schema.md) — The 26-section schema
- [03-design-levels.md](./03-design-levels.md) — Level 0–4 complexity system
- [20-roadmap.md](./20-roadmap.md) — Phased roadmap
