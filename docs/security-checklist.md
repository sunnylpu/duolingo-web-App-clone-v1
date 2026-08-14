# Operational Security Production Checklist

- [x] No plaintext credentials or secrets committed in Git history
- [x] Environment configuration cleanly loaded via `app/config.py` & `.env.example`
- [x] Production `DEBUG=false` masks Python stack traces and internal SQL details
- [x] Environment-driven CORS restrict origin access (`CORS_ORIGINS`)
- [x] Security headers enforced (`nosniff`, `DENY`, `strict-origin-when-cross-origin`)
- [x] Request payload and pagination bounds enforced on all collection endpoints
- [x] In-process sliding-window rate limiting abstraction exists (`shared/rate_limit.py`)
- [x] All state mutations validate server-side user ownership (`current_user`)
- [x] SQLite foreign keys enforced via `PRAGMA foreign_keys = ON`
- [x] Seed content generation cleanly separated from database schema initialization
- [x] Automated security integration test suite passes (`backend/tests/security/`)
