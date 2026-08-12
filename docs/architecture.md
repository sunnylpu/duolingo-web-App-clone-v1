# Duolingo Clone Architecture Documentation

## Overview

The Duolingo Clone platform is designed as a **Modular Monolith**. This pattern combines the operational simplicity and ease of local development of a single codebase with the strict domain boundaries and encapsulation typical of microservices architectures.

---

## Architectural Principles

1. **Strict Domain Scoping**: Business domains are separated into high-cohesion, low-coupling modules (`user`, `course`, `lesson`, `progress`, `gamification`, `leaderboard`).
2. **Standardized Flow**: Every API request strictly adheres to the execution path:
   $$\text{HTTP Request} \longrightarrow \text{Router} \longrightarrow \text{Service} \longrightarrow \text{Repository} \longrightarrow \text{Database}$$
3. **Database Independence**: Database access is fully encapsulated within the Repository layer. Services never call SQL or SQLAlchemy session operations directly.
4. **Contract-Driven Communication**: Request and response objects are explicitly modeled using Pydantic schemas, enforcing strong runtime validation and API stability.
5. **Shared Foundation**: Core concerns like configuration management, database session lifecycles, global exception handling, request context middleware, logging, and security interfaces reside in `app/shared/`.

---

## Domain Boundaries

```
app/modules/
├── user/          # Identity, profiles, and user management
├── course/        # Language course definitions, units, and structure
├── lesson/        # Individual lessons, exercises, and questions
├── progress/      # User course progress, completed lessons, accuracy tracking
├── gamification/  # XP, streaks, hearts, crowns, and achievements
└── leaderboard/   # Competitive ranking leagues and dynamic scoreboards
```

Each module contains:
- `router.py`: Exposes HTTP endpoints using FastAPI `APIRouter`.
- `service.py`: Contains domain business logic and orchestrates operations.
- `repository.py`: Handles data persistence and database operations.
- `models.py`: Defines SQLAlchemy database entities.
- `schemas.py`: Defines Pydantic validation and serialisation models.
- `tests/`: Module-specific unit and integration tests.

---

## Layer Responsibilities

### 1. Router Layer (`router.py`)
- Defines RESTful HTTP endpoints under `/api/v1/...`.
- Parses query parameters and payload bodies using Pydantic schemas.
- Injects dependencies (services, database sessions) via FastAPI dependency injection.
- Delegates execution to the Service layer and returns HTTP responses.
- *Rule*: Routers **MUST NOT** contain database queries or complex business logic.

### 2. Service Layer (`service.py`)
- Implements core business logic, domain rules, and calculations.
- Coordinates data retrieval and persistence with Repositories.
- Enforces access control and validation constraints.
- *Rule*: Services **MUST NOT** import FastAPI response abstractions or write raw SQL queries.

### 3. Repository Layer (`repository.py`)
- Provides a clean abstraction over data persistence.
- Executes SQLAlchemy queries, inserts, updates, and deletes.
- Converts raw database records to domain models.
- *Rule*: Repositories **MUST NOT** evaluate business logic.

### 4. Models (`models.py`)
- Declarative SQLAlchemy models deriving from `shared.database.Base`.

### 5. Schemas (`schemas.py`)
- Strict Pydantic models for input validation (e.g. `UserCreate`) and output serialization (e.g. `UserResponse`).

---

## Shared Layer (`app/shared/`)

- `database.py`: Manages SQLAlchemy `Engine`, `sessionmaker`, and the FastAPI `get_db` generator.
- `errors.py`: Global exception classes (`AppException`, `NotFoundError`, etc.) and error handler handlers for uniform JSON error responses.
- `middleware.py`: CORS configuration, request tracking via `X-Request-ID`, and request timing logs.
- `logging.py`: Structured application logger outputting formatted diagnostics.
- `security.py`: Security interfaces for password hashing (Argon2 / bcrypt) and JWT token parsing.

---

## Microservices Extraction Strategy

Because each domain module maintains strict boundaries and communicates only via service interfaces or message events, extracting a module (e.g. `lesson`) into a standalone microservice requires minimal code changes:

1. **Isolate Database**: Shift `lesson` tables to a dedicated database instance.
2. **Package Service**: Move `app/modules/lesson/` into a dedicated service container (`lesson-service/`).
3. **Update Client Interfaces**: Replace in-memory service calls from other modules with lightweight HTTP or gRPC client adapters.
4. **Deploy Independently**: Utilize Kubernetes deployment manifests configured under `k8s/`.
