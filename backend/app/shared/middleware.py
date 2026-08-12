import time
import uuid
import logging
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from app.config import settings

logger = logging.getLogger("duolingo.middleware")


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware for attaching correlation X-Request-ID and logging request execution details.
    """

    async def dispatch(self, request: Request, call_next) -> Response:
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        request.state.request_id = request_id

        start_time = time.time()
        response = await call_next(request)
        process_time_ms = round((time.time() - start_time) * 1000, 2)

        response.headers["X-Request-ID"] = request_id
        response.headers["X-Process-Time-MS"] = str(process_time_ms)

        logger.info(
            f"[{request_id}] {request.method} {request.url.path} - Status: {response.status_code} - Duration: {process_time_ms}ms"
        )
        return response


def setup_middleware(app: FastAPI) -> None:
    """Configure CORS and request logging middlewares on FastAPI application."""
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(RequestLoggingMiddleware)
