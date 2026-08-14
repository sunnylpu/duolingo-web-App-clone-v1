# System Architecture Specification

```text
                                FRONTEND (Next.js 14 / React 18)
                                ┌──────────────────────────────┐
                                │  App Router / Tailwind CSS   │
                                └──────────────┬───────────────┘
                                               │ HTTP / REST
                                               ▼
                                 BACKEND (FastAPI / Python 3.14)
                                ┌──────────────────────────────┐
                                │  Middleware & Router Layer   │
                                ├──────────────────────────────┤
                                │  Domain Services & Business  │
                                ├──────────────────────────────┤
                                │ SQLAlchemy ORM Repositories │
                                └──────────────┬───────────────┘
                                               │
                                               ▼
                                   DATABASE (SQLite / PostgreSQL)
                                ┌──────────────────────────────┐
                                │ Relational Tables & FKs      │
                                └──────────────────────────────┘
```

## Curriculum Telemetry Snapshot
- **Flagship Course 🇬🇧 English**: 8 Units, 32 Skills, 96 Lessons, 576 Exercises
- **Expanded Secondary 🇪🇸 Spanish**: 5 Units, 20 Skills, 60 Lessons, 360 Exercises
- **Secondary Course 🇫🇷 French**: 3 Units, 12 Skills, 36 Lessons, 216 Exercises
- **Total Platform Scale**: 16 Units, 64 Skills, 192 Lessons, **1,152 Exercises**
