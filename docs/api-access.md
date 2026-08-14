# API Classification & Access Specification

## Public Learner Endpoints
- `GET /health/live`: Process liveness probe
- `GET /health/ready`: Database readiness probe
- `GET /health`: Health summary
- `GET /metrics`: Prometheus operational metrics
- `GET /api/v1/courses`: Course catalog
- `GET /api/v1/path`: Learner course path
- `GET /api/v1/search`: Content search
- `GET /api/v1/vocabulary`: Vocabulary explorer
- `POST /api/v1/lessons/{id}/start`: Start lesson attempt
- `POST /api/v1/lessons/{id}/exercises/{ex_id}/answer`: Submit exercise answer
- `POST /api/v1/lessons/{id}/complete`: Finalize lesson attempt
- `GET /api/v1/notifications`: User notifications
- `POST /api/v1/notifications/{id}/read`: Mark notification read
- `GET /api/v1/quests/today`: Today's assigned quests
- `GET /api/v1/social/feed`: Social activity feed

## Operations & Admin Endpoints (Internal)
- `GET /api/v1/ops/overview`: Operations & telemetry metrics
- `GET /api/v1/admin/overview`: Operations overview alias
