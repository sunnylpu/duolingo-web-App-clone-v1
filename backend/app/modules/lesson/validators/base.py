import re
from abc import ABC, abstractmethod
from typing import Optional, Any
from dataclasses import dataclass
from app.modules.lesson.models import ExerciseModel


@dataclass
class ValidationResult:
    is_correct: bool
    correct_answer: str
    feedback: Optional[str] = None


class ExerciseValidator(ABC):
    """Abstract base class for all exercise type answer validators."""

    def normalize_text(self, text: str) -> str:
        if not text:
            return ""
        cleaned = text.strip().lower()
        cleaned = re.sub(r"[.!?,\s]+$", "", cleaned)
        cleaned = re.sub(r"^[.!?,\s]+", "", cleaned)
        cleaned = re.sub(r"\s+", " ", cleaned)
        return cleaned

    @abstractmethod
    def validate(self, exercise: ExerciseModel, submitted_answer: Any) -> ValidationResult:
        """Evaluates submitted answer against exercise data and returns ValidationResult."""
        pass
