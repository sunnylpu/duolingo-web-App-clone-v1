from typing import Dict
from app.modules.lesson.validators.base import ExerciseValidator
from app.modules.lesson.validators.multiple_choice import MultipleChoiceValidator
from app.modules.lesson.validators.type_answer import TypeAnswerValidator
from app.modules.lesson.validators.translate import TranslateValidator
from app.modules.lesson.validators.word_bank import WordBankValidator
from app.modules.lesson.validators.match_pairs import MatchPairsValidator
from app.modules.lesson.validators.fill_blank import FillBlankValidator


class ValidatorRegistry:
    """Registry mapping exercise types to their respective validator implementations."""

    def __init__(self):
        self._validators: Dict[str, ExerciseValidator] = {
            "multiple_choice": MultipleChoiceValidator(),
            "type_answer": TypeAnswerValidator(),
            "translate": TranslateValidator(),
            "word_bank": WordBankValidator(),
            "match_pairs": MatchPairsValidator(),
            "fill_blank": FillBlankValidator(),
        }

    def get_validator(self, exercise_type: str) -> ExerciseValidator:
        validator = self._validators.get(exercise_type)
        if not validator:
            # Fallback default validator using basic text comparison
            return MultipleChoiceValidator()
        return validator


# Singleton instance for backend reuse
validator_registry = ValidatorRegistry()
