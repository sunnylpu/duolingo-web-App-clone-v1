# Production Security Architecture Specification

## 1. Overview
This document defines the security architecture, data boundaries, and threat mitigation strategy for the Duolingo Web Application API.

---

## 2. Threat Model & Risk Mitigations

| Threat Vector | Mitigation Strategy | Implemented Mechanism |
|---|---|---|
| XSS / Script Injection | Strict output escaping, Content-Security-Policy & Security Headers | `SecurityHeadersMiddleware` |
| CSRF & Cross-Domain Tampering | Restrictive environment-driven CORS origin matching | `CORSMiddleware` in `middleware.py` |
| SQL Injection | Parameterized SQLAlchemy ORM queries exclusively | `SQLAlchemy` ORM queries across repositories |
| Unbounded Payload Attacks | Bounded string lengths & query parameter limit capping | Pydantic schemas & FastAPI Query limits |
| State-Tampering Attacks | Derive all mutation user identity from `current_user` auth | Server-side user ownership checks |
| Database Corruption | Enforced SQLite Foreign Keys | `PRAGMA foreign_keys = ON` |
| Data Leakage | Exception handler stack trace masking when `DEBUG=false` | Unified `AppError` response envelope |

---

## 3. Authorization Matrix

| Endpoint / Action | Access Level | Authorization Rule |
|---|---|---|
| Start / Complete Lesson | Learner | Current user owns attempt & prerequisite is unlocked |
| Submit Exercise Answer | Learner | Current user owns attempt |
| Heart Practice / Refill | Learner | Current user stats |
| Notification Read | Learner | Current user owns notification ID |
| Follow / Unfollow User | Learner | Current user is the follower |
| Public Profile View | Public | Returns non-sensitive public stats & streak only |
| Ops Telemetry (`/ops/overview`) | Admin / Internal | Ops overview telemetry |

---

## 4. Rate Limiting Strategy
State mutation endpoints (exercise answers, practice recovery, heart refill) use a sliding-window rate limiter (`RateLimiter` in `app/shared/rate_limit.py`). In multi-replica Kubernetes deployments, rate-limiting state transitions cleanly to Redis.
