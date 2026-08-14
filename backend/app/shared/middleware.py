import time
import uuid
import json
import logging
from urllib.parse import urlparse
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from app.config import settings
from app.shared.metrics import metrics_registry

logger = logging.getLogger("duolingo.api")


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware for attaching correlation X-Request-ID, measuring timing,
    incrementing metrics, and generating structured logs.
    """

    async def dispatch(self, request: Request, call_next) -> Response:
        request_id = request.headers.get("X-Request-ID")
        if not request_id:
            request_id = f"req_{uuid.uuid4().hex[:12]}"
        request.state.request_id = request_id

        start_time = time.time()
        metrics_registry.increment("requests_total")

        try:
            response = await call_next(request)
        except Exception as exc:
            metrics_registry.increment("request_errors_total")
            raise exc

        process_time_ms = round((time.time() - start_time) * 1000, 2)
        response.headers["X-Request-ID"] = request_id
        response.headers["X-Process-Time-MS"] = str(process_time_ms)

        if response.status_code >= 400:
            metrics_registry.increment("request_errors_total")

        # Structured Log Format
        log_payload = {
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "level": "INFO" if response.status_code < 400 else "ERROR",
            "service": "duolingo-api",
            "request_id": request_id,
            "method": request.method,
            "path": request.url.path,
            "status_code": response.status_code,
            "duration_ms": process_time_ms,
        }

        slow_threshold = getattr(settings, "SLOW_REQUEST_THRESHOLD_MS", 500)
        if process_time_ms > slow_threshold:
            log_payload["level"] = "WARN"
            log_payload["tag"] = "SLOW_REQUEST"
            logger.warning(json.dumps(log_payload))
        else:
            logger.info(json.dumps(log_payload))

        return response


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """
    Middleware for adding modern HTTP security headers to all responses.
    """

    async def dispatch(self, request: Request, call_next) -> Response:
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        return response


class CSRFProtectionMiddleware(BaseHTTPMiddleware):
    """
    CSRF defense for cookie-authenticated state-changing operations.
    Validates Origin/Referer and X-Requested-With headers when session cookie is used.
    """

    EXEMPT_PATHS = {
        f"{settings.API_PREFIX}/auth/login",
        f"{settings.API_PREFIX}/auth/register",
        f"{settings.API_PREFIX}/auth/token",
    }

    async def dispatch(self, request: Request, call_next) -> Response:
        if request.method in {"POST", "PUT", "PATCH", "DELETE"}:
            # Only enforce if request relies on cookie authentication
            has_cookie_session = bool(request.cookies.get("auth_token"))
            has_bearer_auth = bool(request.headers.get("authorization"))

            if has_cookie_session and not has_bearer_auth and request.url.path not in self.EXEMPT_PATHS:
                origin = request.headers.get("origin")
                referer = request.headers.get("referer")
                req_with = request.headers.get("x-requested-with")
                sec_site = request.headers.get("sec-fetch-site")

                # Allowed if custom header is present (browser AJAX) or same-origin/site
                is_safe_ajax = req_with == "XMLHttpRequest" or sec_site in {"same-origin", "same-site"}

                is_valid_origin = False
                if origin:
                    is_valid_origin = any(
                        origin.startswith(allowed.rstrip("/"))
                        for allowed in settings.cors_origins_list
                    )
                elif referer:
                    ref_host = urlparse(referer).netloc
                    is_valid_origin = any(
                        ref_host in allowed
                        for allowed in settings.cors_origins_list
                    )

                # Reject if neither safe origin nor AJAX header is verified
                if not (is_safe_ajax or is_valid_origin):
                    return JSONResponse(
                        status_code=403,
                        content={
                            "error": {
                                "code": "CSRF_REJECTED",
                                "message": "Cross-site request forgery protection rejected this request.",
                            }
                        },
                    )

        return await call_next(request)


def setup_middleware(app: FastAPI) -> None:
    """Configure CORS, request logging, security headers, and CSRF middlewares on FastAPI application."""
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(RequestLoggingMiddleware)
    app.add_middleware(SecurityHeadersMiddleware)
    app.add_middleware(CSRFProtectionMiddleware)
