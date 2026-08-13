"""
Unit Generator — converts UnitSpec into a seed-ready unit dict.
"""

from typing import Dict, Any
from seed.generators import UnitSpec
from seed.generators.skill_generator import generate_skill


def generate_unit(
    unit: UnitSpec,
    course_code: str,
    target_lang_label: str,
    source_lang_label: str = "English",
) -> Dict[str, Any]:
    """
    Convert a UnitSpec into a seed-compatible unit dict.

    Returns:
        {
            "id": str,
            "title": str,
            "description": str,
            "order_index": int,
            "skills": [ skill dicts ]
        }
    """
    skills = [
        generate_skill(skill, course_code, target_lang_label, source_lang_label)
        for skill in unit.skills
    ]
    return {
        "id": unit.id,
        "title": unit.title,
        "description": unit.description,
        "order_index": unit.order_index,
        "skills": skills,
    }
