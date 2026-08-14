# Duolingo Clone — Production-Ready Full-Stack Platform (v1.0.0-rc1)

A production-engineered Duolingo-style language-learning web application built as a scalable **Modular Monolith** with Next.js 14 App Router, FastAPI, SQLAlchemy 2.0, Prometheus metrics, structured audit logging, and production security hardening.

---

## 🚀 Key Platform Features

- **Multi-Course Curriculum Engine**:
  - 🇬🇧 **English Flagship**: 8 Units, 32 Skills, 96 Lessons, 576 Exercises
  - 🇪🇸 **Spanish Expanded**: 5 Units, 20 Skills, 60 Lessons, 360 Exercises
  - 🇫🇷 **French Secondary**: 3 Units, 12 Skills, 36 Lessons, 216 Exercises
  - **Total Scale**: 16 Units, 64 Skills, 192 Lessons, **1,152 Exercises**
- **Lesson Engine & Interactive Exercise Types**:
  - 6 exercise mechanics: Multiple Choice, Word Order, Fill in the Blank, Listening, Speaking, and Matching Pairs.
  - Adaptive difficulty, lazy heart regeneration, practice recovery mode, and Smart Review queue.
- **Gamification & Engagement Layer**:
  - XP rewards, daily streaks, quest missions, weekly challenge, leaderboard rankings, and 29 achievements.
- **Social Learning Platform**:
  - User follow/following network, public profile views, and activity event feed.
- **Content Discovery & Navigation**:
  - Full-text content search, Vocabulary Explorer by course, and multi-course switcher.
- **Production Observability & Telemetry**:
  - `X-Request-ID` request correlation & process timing middleware.
  - Prometheus-compatible metrics endpoint (`GET /metrics`).
  - Transactional operational audit trail (`AuditEventModel`).
  - Liveness & Readiness health probes (`GET /health/live`, `GET /health/ready`).
  - Real-time Operations Dashboard (`/ops` & `/admin`).
- **Production Security & Hardening**:
  - Sliding-window rate-limiting abstraction (`RateLimiter`).
  - Environment-driven CORS policies and strict HTTP security headers (`nosniff`, `DENY`, `strict-origin-when-cross-origin`).
  - Enforced SQLite Foreign Keys (`PRAGMA foreign_keys = ON`).

---

## 🛠️ Technology Stack

### Frontend
- **Framework**: Next.js 14+ (App Router)
- **Language**: TypeScript
- **Styling**: Vanilla CSS / Tailwind CSS design system
- **API Client**: Centralized Fetch client with request correlation

### Backend
- **Framework**: FastAPI
- **Server**: Uvicorn
- **ORM**: SQLAlchemy 2.0
- **Validation**: Pydantic V2
- **Database**: SQLite (Development foundation, PostgreSQL migration ready)
- **Testing**: Pytest & Async Client (117 integration & security tests)

---

## 💻 Local Setup & Execution

### 1. Backend Setup

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Start FastAPI production/dev server
uvicorn app.main:app --reload --port 8000
```

- API Docs (Swagger): `http://localhost:8000/docs`
- Health Probe: `http://localhost:8000/health/live`
- Readiness Probe: `http://localhost:8000/health/ready`
- Metrics: `http://localhost:8000/metrics`

### 2. Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

- Web Application: `http://localhost:3000`
- Ops Dashboard: `http://localhost:3000/ops`

---

## 🧪 Verification & Release Check

Run the canonical automated release verification script:

```bash
./scripts/release-check.sh
```

This validates:
1. All 117 Pytest backend unit, integration, and security tests pass.
2. Deterministic curriculum seed verification passes (`python3 -m seed.verify`).
3. Next.js production build succeeds (`npm run build`).

---

## 📚 System Documentation

- [docs/architecture.md](docs/architecture.md): System architecture & curriculum telemetry snapshot.
- [docs/domain-ownership.md](docs/domain-ownership.md): Domain ownership & event topology.
- [docs/api-inventory.md](docs/api-inventory.md): Complete API endpoint inventory.
- [docs/security.md](docs/security.md): Production security architecture & threat matrix.
- [docs/security-checklist.md](docs/security-checklist.md): Operational security verification checklist.
- [docs/deployment-architecture.md](docs/deployment-architecture.md): Docker, Jenkins CI/CD, Kubernetes & AWS deployment pipeline.
