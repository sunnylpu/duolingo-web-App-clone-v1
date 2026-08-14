import threading
from typing import Dict, Any


class MetricsRegistry:
    """In-process metrics abstraction providing Prometheus-compatible metric counters and gauges."""

    def __init__(self):
        self._lock = threading.Lock()
        self._counters: Dict[str, float] = {
            "requests_total": 0.0,
            "request_errors_total": 0.0,
            "lesson_starts_total": 0.0,
            "lesson_completions_total": 0.0,
            "exercise_answers_total": 0.0,
            "exercise_correct_total": 0.0,
            "exercise_incorrect_total": 0.0,
            "heart_losses_total": 0.0,
            "xp_awarded_total": 0.0,
            "quests_completed_total": 0.0,
            "achievements_unlocked_total": 0.0,
        }

    def increment(self, name: str, value: float = 1.0) -> None:
        with self._lock:
            self._counters[name] = self._counters.get(name, 0.0) + value

    def observe(self, name: str, value: float) -> None:
        self.increment(name, value)

    def get_value(self, name: str) -> float:
        with self._lock:
            return self._counters.get(name, 0.0)

    def get_all_metrics(self) -> Dict[str, float]:
        with self._lock:
            return dict(self._counters)

    def generate_prometheus_text(self) -> str:
        lines = []
        with self._lock:
            for name, val in self._counters.items():
                prom_name = f"duolingo_{name}"
                lines.append(f"# TYPE {prom_name} counter")
                lines.append(f"{prom_name} {int(val) if val.is_integer() else val}")
        return "\n".join(lines) + "\n"


# Global singleton instance
metrics_registry = MetricsRegistry()
