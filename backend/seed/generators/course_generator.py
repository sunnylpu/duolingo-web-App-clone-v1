"""
Course Generator — converts a CourseSpec into a full seed-ready course dict.
Entry point for programmatic course generation.

Usage:
    from seed.generators.course_generator import generate_course
    from seed.catalogs.spanish import SPANISH_COURSE_SPEC

    course_data = generate_course(SPANISH_COURSE_SPEC)
    # course_data matches the COURSE_DATA format used by seed.py
"""

from typing import Dict, Any
from seed.generators import CourseSpec
from seed.generators.unit_generator import generate_unit


def generate_course(spec: CourseSpec) -> Dict[str, Any]:
    """
    Convert a CourseSpec into a complete seed-compatible course dict.

    The output format matches course_data.py's COURSE_DATA structure,
    so it can be passed directly to seed.py's seeding loop.

    Returns:
        {
            "id": str,
            "name": str,
            "code": str,
            "source_language": str,
            "target_language": str,
            "description": str,
            "units": [ unit dicts with nested skills, lessons, exercises ]
        }
    """
    target_lang_label = spec.name  # e.g. "Spanish", "French", "English"
    source_lang_label = spec.source_language.capitalize()  # e.g. "En" → "English"

    units = [
        generate_unit(unit, spec.code, target_lang_label, source_lang_label)
        for unit in spec.units
    ]

    return {
        "id": spec.id,
        "name": spec.name,
        "code": spec.code,
        "source_language": spec.source_language,
        "target_language": spec.target_language,
        "description": spec.description,
        "units": units,
    }
