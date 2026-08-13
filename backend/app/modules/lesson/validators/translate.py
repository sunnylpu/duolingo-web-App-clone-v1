from typing import Any
from app.modules.lesson.models import ExerciseModel
from app.modules.lesson.validators.base import ExerciseValidator, ValidationResult


class TranslateValidator(ExerciseValidator):
    def validate(self, exercise: ExerciseModel, submitted_answer: Any) -> ValidationResult:
        user_str = str(submitted_answer) if submitted_answer is not None else ""
        norm_user = self.normalize_text(user_str)
        norm_correct = self.normalize_text(exercise.correct_answer)

        accepted_list = []
        if exercise.data and isinstance(exercise.data, dict):
            raw_accepted = exercise.data.get("accepted_answers", [])
            if isinstance(raw_accepted, list):
                accepted_list = [self.normalize_text(ans) for ans in raw_accepted]

        is_correct = (norm_user == norm_correct) or (norm_user in accepted_list)
        return ValidationResult(
            is_correct=is_correct,
            correct_answer=exercise.correct_answer,
        )
