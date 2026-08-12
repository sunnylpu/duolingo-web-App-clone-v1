# Duolingo Clone - Full-Stack Scalable Platform (Phase 01)

A production-oriented Duolingo-style language-learning platform built as a scalable **Modular Monolith** with Next.js App Router, FastAPI, SQLAlchemy, and Docker infrastructure.

---

## Technical Stack

### Frontend
- **Framework**: Next.js 14+ (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **API Client**: Centralized Fetch client using `NEXT_PUBLIC_API_URL`

### Backend
- **Framework**: FastAPI
- **Server**: Uvicorn
- **ORM**: SQLAlchemy 2.0
- **Settings**: Pydantic Settings
- **Validation**: Pydantic V2
- **Database**: SQLite (Development foundation, PostgreSQL-ready)
- **Testing**: Pytest & HTTPX

### Infrastructure & Deployment
- **Containerization**: Docker & Docker Compose
- **Orchestration Preparedness**: Kubernetes (`k8s/`)
- **CI/CD Preparedness**: Jenkins (`jenkins/`)

---

## Repository Structure

```
duolingo-clone/
├── frontend/             # Next.js App Router UI
│   ├── app/              # Routes, layout, pages
│   ├── components/       # Reusable UI components
│   ├── features/         # Feature-specific modules
│   ├── hooks/            # Custom React hooks
│   ├── lib/              # Utilities & API client
│   ├── services/         # Service layer helpers
│   ├── types/            # TypeScript type definitions
│   └── public/           # Static assets
├── backend/              # FastAPI Modular Monolith
│   ├── app/
│   │   ├── main.py       # Application entry point
│   │   ├── config.py     # Pydantic Settings configuration
│   │   ├── shared/       # Shared infra (database, errors, logging, security)
│   │   └── modules/      # Domain modules (user, course, lesson, progress, gamification, leaderboard)
│   ├── seed/             # Database seed routines
│   ├── tests/            # Suite of Pytest integration tests
│   ├── requirements.txt  # Python dependencies
│   ├── pytest.ini        # Pytest configuration
│   └── Dockerfile        # Container image specification
├── docker/               # Container tooling & configs
├── k8s/                  # Kubernetes manifest templates
├── jenkins/              # Jenkinsfile pipeline template
├── docs/                 # Architecture, API & Database documentation
├── docker-compose.yml    # Full-stack orchestration
└── README.md             # Project documentation
```

---

## Local Setup & Quickstart

### Prerequisites
- Node.js 18+ & npm
- Python 3.11+
- Docker & Docker Compose (Optional for containerized run)

### 1. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start FastAPI dev server
uvicorn app.main:app --reload --port 8000
```

- API Base URL: `http://localhost:8000`
- Health Endpoint: `http://localhost:8000/health`
- Interactive API Docs (Swagger): `http://localhost:8000/docs`

### 2. Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start Next.js dev server
npm run dev
```

- Web App URL: `http://localhost:3000`

---

## Testing

Run the Pytest suite for the backend:

```bash
cd backend
python3 -m pytest -v
```

---

## Docker Compose Quickstart

Run both frontend and backend in isolated Docker containers:

```bash
docker-compose up --build
```

- Frontend: `http://localhost:3000`
- Backend Health: `http://localhost:8000/health`

---

## Environment Variables

### Backend (`backend/.env.example`)
- `APP_NAME`: Name of the FastAPI application.
- `APP_ENV`: Deployment environment (`development`, `production`, `test`).
- `DEBUG`: Boolean flag for debug mode.
- `DATABASE_URL`: Database connection string (`sqlite:///./data/duolingo.db`).
- `CORS_ORIGINS`: Allowed origins for CORS (comma-separated).
- `API_PREFIX`: Global API version prefix (`/api/v1`).

### Frontend (`frontend/.env.example`)
- `NEXT_PUBLIC_API_URL`: Backend API base URL (`http://localhost:8000/api/v1`).
