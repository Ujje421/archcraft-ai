# 19 — Deployment

> Infrastructure, CI/CD, and deployment strategy.

---

## Development Environment

### Prerequisites

| Tool | Version | Purpose |
|---|---|---|
| Node.js | 20+ | Frontend runtime |
| Python | 3.12+ | Backend runtime |
| PostgreSQL | 16+ | Primary database |
| Redis | 7+ | Caching and rate limiting |
| Docker | 24+ | Containerization |
| Docker Compose | 2.20+ | Local orchestration |

### Local Setup

```bash
# Clone repository
git clone https://github.com/your-org/systemdesign.git
cd systemdesign

# Backend setup
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
cp .env.example .env
# Edit .env with your LLM API key

# Database setup
alembic upgrade head
python -m app.knowledge.loader  # Load component knowledge base

# Start backend
uvicorn app.main:app --reload --port 8000

# Frontend setup (new terminal)
cd frontend
npm install
cp .env.example .env.local
npm run dev
```

### Docker Compose (Alternative)

```yaml
# docker-compose.yml

version: '3.9'

services:
  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    environment:
      - VITE_API_URL=http://localhost:8000
    depends_on:
      - backend

  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql+asyncpg://postgres:postgres@db:5432/systemdesign
      - REDIS_URL=redis://redis:6379/0
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - GEMINI_API_KEY=${GEMINI_API_KEY}
    depends_on:
      - db
      - redis

  db:
    image: pgvector/pgvector:pg16
    ports:
      - "5432:5432"
    environment:
      - POSTGRES_DB=systemdesign
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
    volumes:
      - pgdata:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

volumes:
  pgdata:
```

### Environment Variables

```bash
# .env

# Database
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/systemdesign

# Redis
REDIS_URL=redis://localhost:6379/0

# AI Providers
OPENAI_API_KEY=sk-...
GEMINI_API_KEY=AI...
DEFAULT_LLM_PROVIDER=openai    # openai | gemini

# App
APP_ENV=development            # development | staging | production
APP_SECRET_KEY=your-secret-key
CORS_ORIGINS=http://localhost:3000

# Rate Limiting
RATE_LIMIT_ENABLED=true
RATE_LIMIT_GENERATE=10/hour
RATE_LIMIT_AI=60/hour
```

---

## Repository Structure

```
systemdesign/
├── docs/                          # Architecture documentation (this!)
│   ├── 00-product-vision.md
│   ├── 01-product-requirements.md
│   ├── ...
│   └── 20-roadmap.md
│
├── frontend/                      # React + TypeScript
│   ├── src/
│   ├── public/
│   ├── package.json
│   ├── tsconfig.json
│   ├── tailwind.config.ts
│   ├── vite.config.ts
│   └── Dockerfile
│
├── backend/                       # Python FastAPI
│   ├── app/
│   ├── tests/
│   ├── pyproject.toml
│   ├── alembic.ini
│   └── Dockerfile
│
├── docker-compose.yml
├── .github/
│   └── workflows/
│       ├── ci.yml
│       └── deploy.yml
├── .gitignore
└── README.md
```

---

## CI/CD Pipeline

```mermaid
graph LR
    Push["Git Push"]
    Lint["Lint + Type Check"]
    Test["Run Tests"]
    Build["Build Images"]
    Stage["Deploy Staging"]
    Approve["Manual Approval"]
    Prod["Deploy Production"]
    
    Push --> Lint --> Test --> Build --> Stage --> Approve --> Prod
```

### GitHub Actions — CI

```yaml
# .github/workflows/ci.yml

name: CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  backend:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: pgvector/pgvector:pg16
        env:
          POSTGRES_DB: test_systemdesign
          POSTGRES_PASSWORD: postgres
        ports: [5432:5432]
      redis:
        image: redis:7-alpine
        ports: [6379:6379]
    
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      
      - name: Install dependencies
        run: |
          cd backend
          pip install -e ".[dev]"
      
      - name: Lint
        run: |
          cd backend
          ruff check .
          mypy app/
      
      - name: Test
        run: |
          cd backend
          pytest --cov=app tests/
        env:
          DATABASE_URL: postgresql+asyncpg://postgres:postgres@localhost:5432/test_systemdesign
          REDIS_URL: redis://localhost:6379/0

  frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
      
      - name: Install dependencies
        run: |
          cd frontend
          npm ci
      
      - name: Lint
        run: |
          cd frontend
          npm run lint
      
      - name: Type check
        run: |
          cd frontend
          npm run type-check
      
      - name: Build
        run: |
          cd frontend
          npm run build
```

---

## Production Deployment Options

### Option A: Vercel + Railway (Simplest)

| Component | Service | Cost |
|---|---|---|
| Frontend | Vercel | Free tier |
| Backend | Railway | ~$5-20/month |
| PostgreSQL | Railway (managed) | ~$5-10/month |
| Redis | Railway (managed) | ~$5/month |
| **Total** | | **~$15-35/month** |

### Option B: AWS (Scalable)

| Component | Service | Cost |
|---|---|---|
| Frontend | S3 + CloudFront | ~$5/month |
| Backend | ECS Fargate | ~$30-100/month |
| PostgreSQL | RDS | ~$30-100/month |
| Redis | ElastiCache | ~$15-50/month |
| **Total** | | **~$80-255/month** |

### Option C: VPS (Budget)

| Component | Service | Cost |
|---|---|---|
| Everything | Hetzner/DigitalOcean VPS | ~$10-40/month |
| Managed DB | PlanetScale/Neon | Free-$20/month |
| **Total** | | **~$10-60/month** |

---

## Production Checklist

- [ ] Environment variables configured
- [ ] Database migrations applied
- [ ] Knowledge base seeded
- [ ] HTTPS enabled
- [ ] CORS configured for production domain
- [ ] Rate limiting enabled
- [ ] Error tracking (Sentry) configured
- [ ] Logging configured (structured JSON)
- [ ] Health check endpoint (`/health`)
- [ ] Backup strategy for PostgreSQL
- [ ] LLM API key rotation strategy

---

## Monitoring

### Health Check

```python
@app.get("/health")
async def health_check(db: AsyncSession = Depends(get_db)):
    try:
        await db.execute(text("SELECT 1"))
        return {
            "status": "healthy",
            "version": settings.APP_VERSION,
            "database": "connected",
            "redis": "connected",
        }
    except Exception as e:
        return JSONResponse(
            status_code=503,
            content={"status": "unhealthy", "error": str(e)}
        )
```

---

## Related Documents

- [04-architecture-overview.md](./04-architecture-overview.md) — Platform architecture
- [06-backend-architecture.md](./06-backend-architecture.md) — Backend structure
- [05-frontend-architecture.md](./05-frontend-architecture.md) — Frontend structure
