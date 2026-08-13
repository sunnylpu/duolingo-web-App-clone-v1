from typing import Any
from app.modules.lesson.models import ExerciseModel
from app.modules.lesson.validators.base import ExerciseValidator, ValidationResult


class TypeAnswerValidator(ExerciseValidator):
    def validate(self, exercise: ExerciseModel, submitted_answer: Any) -> ValidationResult:
        user_str = str(submitted_answer) if submitted_answer is not None else ""
        norm_user = self.normalize_text(user_str)
        norm_correct = self.normalize_text(exercise.correct_answer)

        is_correct = norm_user == norm_correct
        return ValidationResult(
            is_correct=is_correct,
            correct_answer=exercise.correct_answer,
        )
