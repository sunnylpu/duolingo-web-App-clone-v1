# Complete API Endpoint Inventory

| Domain | Method | Endpoint | Purpose | Access Level |
|---|---|---|---|---|
| **System** | `GET` | `/health` | Application health summary | Public |
| **System** | `GET` | `/health/live` | Process liveness probe | Public |
| **System** | `GET` | `/health/ready` | Database connectivity readiness probe | Public |
| **System** | `GET` | `/metrics` | Prometheus metrics text format | Public |
| **User** | `GET` | `/api/v1/users/me` | Fetch current learner profile | Learner |
| **Course** | `GET` | `/api/v1/courses` | List all available courses | Public |
| **Course** | `GET` | `/api/v1/courses/{id}` | Detailed course structure | Public |
| **Course** | `GET` | `/api/v1/path` | Get learner course path with unit progress | Learner |
| **Lesson** | `POST` | `/api/v1/lessons/{id}/start` | Start lesson attempt session | Learner |
| **Lesson** | `POST` | `/api/v1/lessons/{id}/exercises/{ex_id}/answer` | Submit exercise answer | Learner |
| **Lesson** | `POST` | `/api/v1/lessons/{id}/complete` | Complete lesson attempt session | Learner |
| **Lesson** | `GET` | `/api/v1/lessons/review/smart` | Smart review exercise queue | Learner |
| **Progress** | `GET` | `/api/v1/progress/units` | Unit completion & milestone stats | Learner |
| **Gamification**| `GET` | `/api/v1/gamification/stats` | Learner XP, hearts, streak, gems | Learner |
| **Gamification**| `POST` | `/api/v1/gamification/practice` | Practice exercise for heart recovery | Learner |
| **Gamification**| `POST` | `/api/v1/gamification/hearts/refill` | Full heart refill | Learner |
| **Quests** | `GET` | `/api/v1/quests/today` | Assigned daily quests & weekly challenge | Learner |
| **Notifications**| `GET` | `/api/v1/notifications` | User notification feed & unread count | Learner |
| **Notifications**| `POST` | `/api/v1/notifications/{id}/read` | Mark single notification read | Learner |
| **Social** | `GET` | `/api/v1/social/feed` | Social activity feed | Learner |
| **Social** | `POST` | `/api/v1/social/follow/{user_id}` | Follow target user | Learner |
| **Search** | `GET` | `/api/v1/search` | Search skills, lessons, vocabulary | Public |
| **Vocabulary** | `GET` | `/api/v1/vocabulary` | Vocabulary explorer by course | Public |
| **Ops** | `GET` | `/api/v1/ops/overview` | Operations telemetry dashboard data | Admin / Internal |
