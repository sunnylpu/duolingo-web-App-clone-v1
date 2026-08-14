"""
Lesson Generator — produces lesson data dicts from a SkillSpec.

For each skill it generates 3 lessons following the pedagogical sequence:
    Lesson 1 — Learn    (vocabulary recognition and introduction)
    Lesson 2 — Practice (apply vocabulary in sentence context)
    Lesson 3 — Mastery  (independent production, all exercise types)

Each lesson contains 5–7 exercises.
"""

from typing import List, Dict, Any
from seed.generators import SkillSpec
from seed.generators.exercise_generator import (
    generate_learn_exercises,
    generate_practice_exercises,
    generate_mastery_exercises,
)

LESSON_MINUTES = {"learn": 4, "practice": 5, "mastery": 6}
LESSON_XP = {"learn": 10, "practice": 12, "mastery": 15}

# Preserved legacy ID prefixes for Spanish course backward compatibility
PRESERVED_SPANISH_PREFIXES = {
    "skill_greetings": ("greetings", "gr"),
    "skill_basics": ("basics", "bs"),
    "skill_food": ("food", "fd"),
    "skill_family": ("family", "fm"),
    "skill_directions": ("directions", "dr"),
    "skill_travel": ("travel", "tr"),
}


def generate_lessons_for_skill(
    skill: SkillSpec,
    course_code: str,
    target_lang_label: str,
    source_lang_label: str = "English",
) -> List[Dict[str, Any]]:
    """
    Generate exactly 3 lessons (Learn, Practice, Mastery) for a skill.

    Returns a list of lesson data dicts matching the seed format.
    """
    if course_code == "es" and skill.id in PRESERVED_SPANISH_PREFIXES:
        lsn_tag, ex_tag = PRESERVED_SPANISH_PREFIXES[skill.id]
        lsn_prefix = lsn_tag
        l1_ex_prefix = f"ex_{ex_tag}1"
        l2_ex_prefix = f"ex_{ex_tag}2"
        l3_ex_prefix = f"ex_{ex_tag}3"
    else:
        prefix = f"{course_code}_{skill.id}"
        lsn_prefix = prefix
        l1_ex_prefix = f"ex_{prefix}_l1"
        l2_ex_prefix = f"ex_{prefix}_l2"
        l3_ex_prefix = f"ex_{prefix}_l3"

    # ── Lesson 1: Learn ───────────────────────────────────────────
    learn_exercises = generate_learn_exercises(
        skill=skill,
        lesson_id_prefix=f"lsn_{lsn_prefix}_1",
        ex_id_prefix=l1_ex_prefix,
        target_lang_label=target_lang_label,
    )

    # ── Lesson 2: Practice ────────────────────────────────────────
    practice_exercises = generate_practice_exercises(
        skill=skill,
        lesson_id_prefix=f"lsn_{lsn_prefix}_2",
        ex_id_prefix=l2_ex_prefix,
        source_lang_label=source_lang_label,
    )

    # ── Lesson 3: Mastery ─────────────────────────────────────────
    mastery_exercises = generate_mastery_exercises(
        skill=skill,
        lesson_id_prefix=f"lsn_{lsn_prefix}_3",
        ex_id_prefix=l3_ex_prefix,
        target_lang_label=target_lang_label,
    )

    return [
        {
            "id": f"lsn_{lsn_prefix}_1",
            "title": f"{skill.title} — Learn",
            "description": f"Discover key vocabulary for {skill.title.lower()}.",
            "order_index": 1,
            "xp_reward": LESSON_XP["learn"],
            "estimated_minutes": LESSON_MINUTES["learn"],
            "exercises": learn_exercises,
        },
        {
            "id": f"lsn_{lsn_prefix}_2",
            "title": f"{skill.title} — Practice",
            "description": f"Apply your {skill.title.lower()} knowledge in real sentences.",
            "order_index": 2,
            "xp_reward": LESSON_XP["practice"],
            "estimated_minutes": LESSON_MINUTES["practice"],
            "exercises": practice_exercises,
        },
        {
            "id": f"lsn_{lsn_prefix}_3",
            "title": f"{skill.title} — Mastery",
            "description": f"Prove your mastery of {skill.title.lower()}.",
            "order_index": 3,
            "xp_reward": LESSON_XP["mastery"],
            "estimated_minutes": LESSON_MINUTES["mastery"],
            "exercises": mastery_exercises,
        },
    ]
