"""
Curriculum metadata types shared across all generator modules.

A SkillSpec drives all downstream generation:
  - vocabulary: list of (target_word, source_word) tuples
  - sentences: list of (target_sentence, source_sentence) tuples
  - lesson 1 = Learn   (new vocabulary introduction)
  - lesson 2 = Practice (apply vocabulary in context)
  - lesson 3 = Mastery  (produce language independently)
"""

from dataclasses import dataclass, field
from typing import List, Optional, Tuple


@dataclass
class VocabItem:
    """A single vocabulary pair: target_word ↔ source_word."""
    target: str   # Word in the language being learned
    source: str   # Translation in the learner's language
    hint: Optional[str] = None


@dataclass
class SentenceItem:
    """A full sentence pair for translation/fill-blank exercises."""
    target: str      # Sentence in the language being learned
    source: str      # English/source translation
    words: Optional[List[str]] = None   # Pre-tokenized word bank
    blank_word: Optional[str] = None    # Word to blank out for fill_blank
    blank_before: Optional[str] = None
    blank_after: Optional[str] = None


@dataclass
class SkillSpec:
    """
    Declarative curriculum specification for a single skill.
    Drives lesson and exercise generation — not the raw exercise data itself.
    """
    id: str
    title: str
    description: str
    objective: str          # What the learner can do after mastery
    difficulty: int         # 1 = beginner, 2 = elementary, 3 = intermediate, 4 = upper
    vocabulary: List[VocabItem] = field(default_factory=list)
    sentences: List[SentenceItem] = field(default_factory=list)
    prerequisite_skill_id: Optional[str] = None
    xp_reward: int = 15
    order_index: int = 1


@dataclass
class UnitSpec:
    """Declarative specification for a course unit."""
    id: str
    title: str
    description: str
    order_index: int
    skills: List[SkillSpec] = field(default_factory=list)


@dataclass
class CourseSpec:
    """Top-level course specification."""
    id: str
    name: str
    code: str
    source_language: str
    target_language: str
    description: str
    units: List[UnitSpec] = field(default_factory=list)
