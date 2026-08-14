"""
Adaptive Difficulty & Mastery Scoring Engine for Domain Intelligence (Phase 26).
"""
from typing import Dict, Any


def calculate_mastery_state(mastery_score: float) -> str:
    """
    Map mastery score (0-100) to deterministic mastery state:
    0 - 39   -> weak
    40 - 69  -> developing
    70 - 89  -> strong
    90 - 100 -> mastered
    """
    if mastery_score >= 90.0:
        return "mastered"
    elif mastery_score >= 70.0:
        return "strong"
    elif mastery_score >= 40.0:
        return "developing"
    else:
        return "weak"


def calculate_mastery_score(completion_percent: float, accuracy_percent: float) -> float:
    """
    Deterministic mastery formula:
    mastery_score = 0.5 * completion_percent + 0.5 * accuracy_percent
    """
    score = 0.5 * completion_percent + 0.5 * accuracy_percent
    return float(round(min(100.0, max(0.0, score)), 1))


def recommend_difficulty(current_difficulty: int, accuracy_percent: float) -> int:
    """
    Recommend adaptive difficulty level bounded by current_difficulty +/- 1:
    - accuracy >= 85%: level up (max 3)
    - accuracy < 60%: level down (min 1)
    - otherwise: stay at current_difficulty
    """
    if accuracy_percent >= 85.0:
        return min(3, current_difficulty + 1)
    elif accuracy_percent < 60.0 and accuracy_percent > 0:
        return max(1, current_difficulty - 1)
    return current_difficulty
