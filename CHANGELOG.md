# ArchCraft Changelog

All notable changes to this project will be documented in this file.

## [Unreleased] - 2026-08-20

### Added (Sprint 1-2 Foundation)
- **Documentation**: Generated full architecture documentation (21 Markdown files in `docs/`).
- **Backend Setup**: Scaffolded FastAPI backend with Python 3.12.
- **Database Architecture**: Implemented async SQLAlchemy models for `System`, `ArchNode`, `ArchConnection`, and Knowledge Base `Component`.
- **Capacity Engine**: Implemented deterministic math-based capacity calculator (traffic, bandwidth, storage) with comprehensive Pytest unit tests.
- **Validation Engine**: Added architecture graph validation logic (orphan nodes, dangling connections).
- **Knowledge Base**: Seeded in-memory component database with 20+ infrastructure technologies (PostgreSQL, Kafka, Redis, S3, etc.).
- **Frontend Setup**: Scaffolded React application using Vite, TypeScript, and Tailwind CSS.
- **Design System**: Created dark-mode specific Tailwind tokens (`@theme`) in `index.css`.
- **State Management**: Integrated Zustand for global state (Levels L0-L4, Active System).
- **Interactive Canvas**: Integrated `@xyflow/react` (React Flow) and built a Demo Canvas Page.
- **Routing**: Set up `react-router-dom` with a responsive sidebar layout and HomePage.
