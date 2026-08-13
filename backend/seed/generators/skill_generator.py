"""
Skill Generator — converts SkillSpec into a seed-ready skill dict.
"""

from typing import Dict, Any
from seed.generators import SkillSpec
from seed.generators.lesson_generator import generate_lessons_for_skill


def generate_skill(
    skill: SkillSpec,
    course_code: str,
    target_lang_label: str,
    source_lang_label: str = "English",
) -> Dict[str, Any]:
    """
    Convert a SkillSpec into a seed-compatible skill dict (matching course_data.py format).

    Returns:
        {
            "id": str,
            "title": str,
            "description": str,
            "objective": str,
            "difficulty": int,
            "order_index": int,
            "xp_reward": int,
            "prerequisite_skill_id": str | None,
            "lessons": [ lesson dicts ]
        }
    """
    lessons = generate_lessons_for_skill(
        skill=skill,
        course_code=course_code,
        target_lang_label=target_lang_label,
        source_lang_label=source_lang_label,
    )
    return {
        "id": skill.id,
        "title": skill.title,
        "description": skill.description,
        "objective": skill.objective,
        "difficulty": skill.difficulty,
        "order_index": skill.order_index,
        "xp_reward": skill.xp_reward,
        "prerequisite_skill_id": skill.prerequisite_skill_id,
        "lessons": lessons,
    }
