# Duolingo Platform REST API Reference

Centralized reference for all REST API endpoints served under prefix `/api/v1`.

---

## 1. System & Health Probes

| Endpoint | Method | Description | Response |
|---|---|---|---|
| `/health` | `GET` | Application liveness probe | `{"status": "ok"}` |
| `/health/live` | `GET` | Kubernetes liveness probe | `{"status": "ok"}` |
| `/health/ready` | `GET` | Kubernetes readiness probe (SELECT 1) | `{"status": "ready", "database": "connected"}` |

---

## 2. User & Profile Domain

| Endpoint | Method | Description |
|---|---|---|
| `/api/v1/users/me` | `GET` | Current active user profile |
| `/api/v1/users/me/stats` | `GET` | User gamification statistics |
| `/api/v1/users/me/profile` | `GET` | Aggregated learner profile dashboard |

---

## 3. Course & Path Domain

| Endpoint | Method | Description |
|---|---|---|
| `/api/v1/courses` | `GET` | List active courses |
| `/api/v1/courses/{id}` | `GET` | Get course detail with units |
| `/api/v1/path` | `GET` | Get user learning path with dynamic skill statuses |
| `/api/v1/progress` | `GET` | Get user skill progress summary |

---

## 4. Lesson Player & Exercise Domain

| Endpoint | Method | Description |
|---|---|---|
| `/api/v1/lessons/{id}` | `GET` | Get lesson detail with exercises |
| `/api/v1/lessons/{id}/start` | `POST` | Start or resume lesson attempt |
| `/api/v1/lessons/{id}/exercises/{exercise_id}/answer` | `POST` | Submit answer for exercise validation |
| `/api/v1/lessons/{id}/complete` | `POST` | Complete lesson attempt & trigger rewards |

---

## 5. Gamification & Hearts Domain

| Endpoint | Method | Description |
|---|---|---|
| `/api/v1/gamification/stats` | `GET` | Get gamification stats & heart regeneration status |
| `/api/v1/gamification/daily` | `GET` | Get today's daily activity & goal progress |
| `/api/v1/gamification/practice` | `GET` | Get practice exercise for heart recovery |
| `/api/v1/gamification/practice` | `POST` | Submit practice exercise answer |
| `/api/v1/gamification/hearts/refill` | `POST` | Mock refill hearts to MAX_HEARTS |

---

## 6. Achievements Domain

| Endpoint | Method | Description |
|---|---|---|
| `/api/v1/achievements` | `GET` | List all platform achievements |
| `/api/v1/users/me/achievements` | `GET` | Get user achievements with progress metrics |

---

## 7. Leaderboard Domain

| Endpoint | Method | Description |
|---|---|---|
| `/api/v1/leaderboard` | `GET` | Get period standings (`weekly`, `monthly`, `all_time`) |
| `/api/v1/leaderboard/me` | `GET` | Get current user's rank |

---

## 8. Standard Error Format

All error responses strictly adhere to:

```json
{
  "error": {
    "code": "SKILL_LOCKED",
    "message": "Complete the prerequisite skill first.",
    "details": null
  }
}
```
