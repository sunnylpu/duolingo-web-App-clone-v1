import time
import threading
from typing import Dict, List, Tuple
from app.shared.errors import ValidationError


class RateLimiter:
    """
    In-process sliding-window rate limiting abstraction for state mutation endpoints.
    Designed for easy migration to Redis in multi-replica production environments.
    """

    def __init__(self):
        self._lock = threading.Lock()
        self._records: Dict[str, List[float]] = {}

    def check(self, key: str, limit: int = 60, window_seconds: int = 60) -> bool:
        now = time.time()
        cutoff = now - window_seconds

        with self._lock:
            timestamps = self._records.get(key, [])
            valid_timestamps = [t for t in timestamps if t > cutoff]
            self._records[key] = valid_timestamps
            return len(valid_timestamps) < limit

    def consume(self, key: str, limit: int = 60, window_seconds: int = 60) -> int:
        now = time.time()
        cutoff = now - window_seconds

        with self._lock:
            timestamps = self._records.get(key, [])
            valid_timestamps = [t for t in timestamps if t > cutoff]

            if len(valid_timestamps) >= limit:
                raise ValidationError(
                    "Rate limit exceeded. Please wait before making more requests.",
                    code="RATE_LIMIT_EXCEEDED",
                )

            valid_timestamps.append(now)
            self._records[key] = valid_timestamps
            return limit - len(valid_timestamps)

    def reset(self, key: str) -> None:
        with self._lock:
            self._records.pop(key, None)

    def clear(self) -> None:
        with self._lock:
            self._records.clear()


# Global rate limiter instance
rate_limiter = RateLimiter()
