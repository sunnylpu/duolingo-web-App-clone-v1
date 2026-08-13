from typing import Any, List, Tuple, Set
from app.modules.lesson.models import ExerciseModel
from app.modules.lesson.validators.base import ExerciseValidator, ValidationResult


class MatchPairsValidator(ExerciseValidator):
    def validate(self, exercise: ExerciseModel, submitted_answer: Any) -> ValidationResult:
        # Extract expected pairs from exercise data
        expected_pairs: List[dict] = []
        if exercise.data and isinstance(exercise.data, dict):
            expected_pairs = exercise.data.get("pairs", [])

        # Build normalized set of expected pairs: set of (left, right)
        norm_expected_set: Set[Tuple[str, str]] = set()
        canonical_pairs: List[str] = []

        for p in expected_pairs:
            if isinstance(p, dict):
                left_val = str(p.get("left", ""))
                right_val = str(p.get("right", ""))
                norm_expected_set.add((self.normalize_text(left_val), self.normalize_text(right_val)))
                canonical_pairs.append(f"{left_val} ↔ {right_val}")

        canonical_answer_str = ", ".join(canonical_pairs)

        # Extract submitted pairs from request (can be dict {"pairs": [...]} or list of pairs)
        raw_submitted_pairs: List[Any] = []
        if isinstance(submitted_answer, dict):
            raw_submitted_pairs = submitted_answer.get("pairs", [])
        elif isinstance(submitted_answer, list):
            raw_submitted_pairs = submitted_answer

        norm_submitted_set: Set[Tuple[str, str]] = set()
        for pair_item in raw_submitted_pairs:
            if isinstance(pair_item, (list, tuple)) and len(pair_item) == 2:
                norm_submitted_set.add(
                    (self.normalize_text(str(pair_item[0])), self.normalize_text(str(pair_item[1])))
                )
            elif isinstance(pair_item, dict) and "left" in pair_item and "right" in pair_item:
                norm_submitted_set.add(
                    (
                        self.normalize_text(str(pair_item["left"])),
                        self.normalize_text(str(pair_item["right"])),
                    )
                )

        # Pair matching is order-independent
        is_correct = (norm_expected_set == norm_submitted_set) and len(norm_expected_set) > 0

        return ValidationResult(
            is_correct=is_correct,
            correct_answer=canonical_answer_str or (exercise.correct_answer or "Matched Pairs"),
        )
