from datetime import datetime, timezone
import zoneinfo
from app.config import settings


class Clock:
    """Base clock interface for system and test time providers."""
    def now(self) -> datetime:
        raise NotImplementedError


class SystemClock(Clock):
    """Production system clock using UTC / APP_TIMEZONE."""
    def now(self) -> datetime:
        try:
            tz = zoneinfo.ZoneInfo(settings.APP_TIMEZONE)
            return datetime.now(tz)
        except Exception:
            return datetime.now(timezone.utc)


class MockClock(Clock):
    """Controllable mock clock for fast, sleep-free unit testing."""
    def __init__(self, current_time: datetime):
        self._current_time = current_time

    def now(self) -> datetime:
        return self._current_time

    def set_time(self, new_time: datetime):
        self._current_time = new_time

    def advance(self, **kwargs):
        from datetime import timedelta
        self._current_time += timedelta(**kwargs)


# Global default clock instance
system_clock = SystemClock()
