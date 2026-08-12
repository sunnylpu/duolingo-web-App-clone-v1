# Duolingo Clone API Documentation (Phase 03)

## Versioning & Base URL

All application endpoints are versioned under:
`http://localhost:8000/api/v1`

Interactive Swagger UI: `http://localhost:8000/docs`
ReDoc Documentation: `http://localhost:8000/redoc`

---

## Architecture Flow

Every API endpoint follows strict layer separation:
$$\text{HTTP Request} \longrightarrow \text{FastAPI Router} \longrightarrow \text{Domain Service} \longrightarrow \text{Domain Repository} \longrightarrow \text{SQLAlchemy} \longrightarrow \text{SQLite/PostgreSQL}$$

---

## Summary of Versioned Endpoints

| Group | Method | Endpoint | Description |
| :--- | :--- | :--- | :--- |
| **System** | `GET` | `/health` | Application health check |
| **Users** | `GET` | `/api/v1/users/me` | Current demo learner profile |
| **Users** | `GET` | `/api/v1/users/me/stats` | Current demo learner statistics |
| **Courses** | `GET` | `/api/v1/courses` | List all active language courses |
| **Courses** | `GET` | `/api/v1/courses/{course_id}` | Detailed course info with unit list |
| **Learning Path**| `GET` | `/api/v1/path` | Structured learning path (Course -> Units -> Skills) |
| **Lessons** | `GET` | `/api/v1/lessons/{lesson_id}` | Lesson details with all exercises |
| **Progress** | `GET` | `/api/v1/progress` | User skill progress summary |
| **Gamification** | `GET` | `/api/v1/gamification/stats` | Read-only XP, streak, hearts, gems stats |
| **Leaderboard** | `GET` | `/api/v1/leaderboard` | Ranked standings (`?period=weekly\|monthly\|all_time`) |
| **Achievements** | `GET` | `/api/v1/achievements` | Platform achievements definition list |
| **Achievements** | `GET` | `/api/v1/users/me/achievements` | Achievements unlocked by current learner |

---

## Endpoint Payload Examples

### 1. Current Demo Learner Profile
`GET /api/v1/users/me`
```json
{
  "id": "usr_demo",
  "username": "demolearner",
  "display_name": "Demo Learner",
  "email": "demo@duolingo.clone",
  "avatar": "https://api.dicebear.com/7.x/bottts/svg?seed=demolearner",
  "is_active": true
}
```

### 2. User Stats
`GET /api/v1/users/me/stats`
```json
{
  "total_xp": 150,
  "current_streak": 7,
  "longest_streak": 12,
  "hearts": 5,
  "gems": 450,
  "daily_goal_xp": 20,
  "daily_xp": 25
}
```

### 3. Learning Path
`GET /api/v1/path`
```json
{
  "course": {
    "id": "crs_spanish",
    "name": "Spanish",
    "code": "es",
    "source_language": "en",
    "target_language": "es",
    "description": "Learn Spanish from scratch",
    "is_active": true
  },
  "units": [
    {
      "id": "unit_01",
      "title": "Unit 1: Greetings & Introduction",
      "description": "Master basic greetings",
      "order_index": 1,
      "skills": [
        {
          "id": "skill_greetings",
          "title": "Greetings",
          "description": "Say hello and goodbye",
          "order_index": 1,
          "xp_reward": 15,
          "prerequisite_skill_id": null,
          "status": "completed",
          "completion_percent": 100.0,
          "crown_level": 1
        }
      ]
    }
  ]
}
```

### 4. Lesson Details & Exercises
`GET /api/v1/lessons/lsn_greetings_1`
```json
{
  "id": "lsn_greetings_1",
  "skill_id": "skill_greetings",
  "title": "Basic Hello",
  "description": "Learn common greetings.",
  "order_index": 1,
  "xp_reward": 10,
  "estimated_minutes": 3,
  "exercises": [
    {
      "id": "ex_gr1_1",
      "type": "multiple_choice",
      "prompt": "What does 'hola' mean?",
      "correct_answer": "Hello",
      "data": { "options": ["Hello", "Goodbye", "Thanks", "Please"] },
      "order_index": 1,
      "xp_reward": 5
    }
  ]
}
```

### 5. Leaderboard Standings
`GET /api/v1/leaderboard?period=weekly`
```json
{
  "period": "weekly",
  "entries": [
    {
      "rank": 1,
      "user_id": "usr_polyglot",
      "username": "polyglotpete",
      "display_name": "Polyglot Pete",
      "avatar": "https://api.dicebear.com/7.x/bottts/svg?seed=polyglotpete",
      "xp": 340
    }
  ]
}
```

---

## Standard Error Response Format

Errors return a consistent JSON schema:
```json
{
  "error": {
    "code": "NOT_FOUND",
    "message": "Course with ID 'invalid_id' was not found.",
    "details": null
  }
}
```

### Standard Status Codes
- `HTTP 200 OK`: Successful retrieval
- `HTTP 400 Bad Request`: Validation error (e.g. invalid query parameter)
- `HTTP 404 Not Found`: Resource does not exist
- `HTTP 500 Internal Server Error`: Server failure masked securely
