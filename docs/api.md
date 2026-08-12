# Duolingo Clone API Documentation

## API Versioning & Endpoints

All application API endpoints are versioned under the `/api/v1` prefix (configurable via `API_PREFIX` environment variable).

Swagger UI interactive documentation is available at:
`GET /docs`

ReDoc documentation is available at:
`GET /redoc`

---

## Standard Health Endpoint

### `GET /health`

- **Description**: Returns application operational status.
- **Authentication**: Public
- **Response**: `200 OK`
- **Response Body**:
  ```json
  {
    "status": "ok"
  }
  ```

---

## Domain Endpoint Prefixes (Phase 01 Scaffolding)

| Domain | Base Path | Description |
| :--- | :--- | :--- |
| **User** | `/api/v1/users` | User identity and profile management |
| **Course** | `/api/v1/courses` | Language courses, units, and curriculum |
| **Lesson** | `/api/v1/lessons` | Lessons, exercises, and interactive content |
| **Progress** | `/api/v1/progress` | User completion state and accuracy metrics |
| **Gamification** | `/api/v1/gamification` | XP, streaks, hearts, crowns, and gems |
| **Leaderboard** | `/api/v1/leaderboard` | Leagues and competitive standings |

---

## Standard Error Response Format

All API errors return a uniform JSON payload structure:

```json
{
  "error": {
    "code": "NOT_FOUND",
    "message": "Resource was not found.",
    "details": null
  }
}
```

### Standard Error Codes
- `BAD_REQUEST`: Invalid inputs or request formatting (`HTTP 400`)
- `UNAUTHORIZED`: Authentication missing or invalid (`HTTP 401`)
- `FORBIDDEN`: Insufficient permissions (`HTTP 403`)
- `NOT_FOUND`: Requested entity does not exist (`HTTP 404`)
- `INTERNAL_SERVER_ERROR`: Unhandled application failure (`HTTP 500`)
