"""
Exercise Generator — produces exercise dicts compatible with the existing
ExerciseModel schema and unified ValidatorRegistry.

Each generator function receives curriculum context (SkillSpec, vocabulary,
sentences) and returns a list of exercise data dicts ready for database insertion.

All 6 types are supported:
    multiple_choice | type_answer | translate | word_bank | match_pairs | fill_blank
"""

from typing import List, Dict, Any, Optional
import random
from seed.generators import SkillSpec, VocabItem, SentenceItem


# ── Helper ────────────────────────────────────────────────────────────────────

def _distractors(correct: str, pool: List[str], n: int = 3) -> List[str]:
    """Return n distractor options that are not the correct answer."""
    others = [w for w in pool if w != correct]
    selected = others[:n]
    # Pad with generic fillers if pool is too small
    while len(selected) < n:
        selected.append(f"option_{len(selected)}")
    return selected


# ── Individual exercise builders ───────────────────────────────────────────────

def build_multiple_choice(
    ex_id: str,
    order_index: int,
    prompt: str,
    correct_answer: str,
    options: List[str],
    xp_reward: int = 5,
) -> Dict[str, Any]:
    """Multiple-choice question with 4 options (correct + 3 distractors)."""
    shuffled = list({correct_answer} | set(options))
    random.shuffle(shuffled)
    return {
        "id": ex_id,
        "type": "multiple_choice",
        "prompt": prompt,
        "correct_answer": correct_answer,
        "data": {"options": shuffled},
        "order_index": order_index,
        "xp_reward": xp_reward,
    }


def build_type_answer(
    ex_id: str,
    order_index: int,
    prompt: str,
    correct_answer: str,
    hint: Optional[str] = None,
    xp_reward: int = 5,
) -> Dict[str, Any]:
    """Free-text type answer with optional hint."""
    return {
        "id": ex_id,
        "type": "type_answer",
        "prompt": prompt,
        "correct_answer": correct_answer,
        "data": {"hint": hint or ""},
        "order_index": order_index,
        "xp_reward": xp_reward,
    }


def build_translate(
    ex_id: str,
    order_index: int,
    prompt: str,
    source_text: str,
    correct_answer: str,
    accepted_answers: Optional[List[str]] = None,
    xp_reward: int = 5,
) -> Dict[str, Any]:
    """Translation exercise — translate the source_text into target language."""
    return {
        "id": ex_id,
        "type": "translate",
        "prompt": prompt,
        "correct_answer": correct_answer,
        "data": {
            "source_text": source_text,
            "accepted_answers": accepted_answers or [correct_answer],
        },
        "order_index": order_index,
        "xp_reward": xp_reward,
    }


def build_word_bank(
    ex_id: str,
    order_index: int,
    prompt: str,
    correct_answer: str,
    words: List[str],
    xp_reward: int = 5,
) -> Dict[str, Any]:
    """Word-bank: tap words in order to build the correct answer."""
    shuffled = list(words)
    random.shuffle(shuffled)
    return {
        "id": ex_id,
        "type": "word_bank",
        "prompt": prompt,
        "correct_answer": correct_answer,
        "data": {"words": shuffled},
        "order_index": order_index,
        "xp_reward": xp_reward,
    }


def build_match_pairs(
    ex_id: str,
    order_index: int,
    prompt: str,
    pairs: List[Dict[str, str]],
    xp_reward: int = 5,
) -> Dict[str, Any]:
    """Match-pairs: connect left column to right column."""
    correct_answer = ", ".join(f"{p['left']} ↔ {p['right']}" for p in pairs)
    return {
        "id": ex_id,
        "type": "match_pairs",
        "prompt": prompt,
        "correct_answer": correct_answer,
        "data": {"pairs": pairs},
        "order_index": order_index,
        "xp_reward": xp_reward,
    }


def build_fill_blank(
    ex_id: str,
    order_index: int,
    prompt: str,
    correct_answer: str,
    sentence_before: str,
    sentence_after: str,
    options: Optional[List[str]] = None,
    xp_reward: int = 5,
) -> Dict[str, Any]:
    """Fill-in-the-blank: complete the sentence with the correct word."""
    data: Dict[str, Any] = {
        "sentence_before": sentence_before,
        "blank": "___",
        "sentence_after": sentence_after,
    }
    if options:
        data["options"] = options
    return {
        "id": ex_id,
        "type": "fill_blank",
        "prompt": prompt,
        "correct_answer": correct_answer,
        "data": data,
        "order_index": order_index,
        "xp_reward": xp_reward,
    }


# ── High-level: generate a full set of exercises for one lesson ────────────────

def generate_learn_exercises(
    skill: SkillSpec,
    lesson_id_prefix: str,
    ex_id_prefix: str,
    target_lang_label: str = "the target language",
) -> List[Dict[str, Any]]:
    """
    Lesson 1 — Learn: Introduce new vocabulary through recognition exercises.
    Produces 5–7 exercises mixing multiple_choice and match_pairs.
    """
    vocab = skill.vocabulary
    all_targets = [v.target for v in vocab]
    all_sources = [v.source for v in vocab]
    exercises = []
    order = 1

    # Multiple choice: source → target recognition
    for i, item in enumerate(vocab[:4]):
        distractors = _distractors(item.target, all_targets, 3)
        options = [item.target] + distractors
        exercises.append(build_multiple_choice(
            ex_id=f"{ex_id_prefix}_mc_{i+1}",
            order_index=order,
            prompt=f"What does '{item.source}' mean in {target_lang_label}?",
            correct_answer=item.target,
            options=options,
        ))
        order += 1

    # Match pairs: group 3 at a time
    if len(vocab) >= 3:
        pairs = [{"left": v.source, "right": v.target} for v in vocab[:3]]
        exercises.append(build_match_pairs(
            ex_id=f"{ex_id_prefix}_mp_1",
            order_index=order,
            prompt="Match the words to their translations:",
            pairs=pairs,
        ))
        order += 1

    # Type answer: production
    if vocab:
        item = vocab[0]
        exercises.append(build_type_answer(
            ex_id=f"{ex_id_prefix}_ta_1",
            order_index=order,
            prompt=f"Type in {target_lang_label}: '{item.source}'",
            correct_answer=item.target,
            hint=item.hint,
        ))
        order += 1

    return exercises


def generate_practice_exercises(
    skill: SkillSpec,
    lesson_id_prefix: str,
    ex_id_prefix: str,
    source_lang_label: str = "English",
) -> List[Dict[str, Any]]:
    """
    Lesson 2 — Practice: Apply vocabulary in sentence context.
    Produces 5–7 exercises mixing word_bank, translate, and fill_blank.
    """
    sentences = skill.sentences
    vocab = skill.vocabulary
    exercises = []
    order = 1

    # Word bank: build sentences
    for i, sent in enumerate(sentences[:3]):
        words = sent.words or sent.target.split()
        # Add distractors from vocab
        distractors = [v.target for v in vocab if v.target not in words][:2]
        bank = words + distractors
        exercises.append(build_word_bank(
            ex_id=f"{ex_id_prefix}_wb_{i+1}",
            order_index=order,
            prompt=f"Translate to target language: '{sent.source}'",
            correct_answer=sent.target,
            words=bank,
        ))
        order += 1

    # Translate: full sentence
    for i, sent in enumerate(sentences[1:3]):
        exercises.append(build_translate(
            ex_id=f"{ex_id_prefix}_tr_{i+1}",
            order_index=order,
            prompt=f"Translate: '{sent.target}'",
            source_text=sent.target,
            correct_answer=sent.source,
            accepted_answers=[sent.source, sent.source + "."],
        ))
        order += 1

    # Fill blank: one sentence
    if sentences and sentences[0].blank_word:
        sent = sentences[0]
        exercises.append(build_fill_blank(
            ex_id=f"{ex_id_prefix}_fb_1",
            order_index=order,
            prompt="Complete the sentence:",
            correct_answer=sent.blank_word,
            sentence_before=sent.blank_before or "",
            sentence_after=sent.blank_after or "",
        ))
        order += 1

    return exercises


def generate_mastery_exercises(
    skill: SkillSpec,
    lesson_id_prefix: str,
    ex_id_prefix: str,
    target_lang_label: str = "the target language",
) -> List[Dict[str, Any]]:
    """
    Lesson 3 — Mastery: Independent production with all exercise types.
    Produces 5–7 exercises across all 6 types.
    """
    vocab = skill.vocabulary
    sentences = skill.sentences
    all_targets = [v.target for v in vocab]
    all_sources = [v.source for v in vocab]
    exercises = []
    order = 1

    # Multiple choice: harder prompt (target → source)
    if vocab:
        item = vocab[-1]  # Use last (harder) vocab item
        distractors = _distractors(item.source, all_sources, 3)
        exercises.append(build_multiple_choice(
            ex_id=f"{ex_id_prefix}_mc_1",
            order_index=order,
            prompt=f"What does '{item.target}' mean?",
            correct_answer=item.source,
            options=[item.source] + distractors,
        ))
        order += 1

    # Type answer: production from English
    if len(vocab) >= 2:
        item = vocab[1]
        exercises.append(build_type_answer(
            ex_id=f"{ex_id_prefix}_ta_1",
            order_index=order,
            prompt=f"Type in {target_lang_label}: '{item.source}'",
            correct_answer=item.target,
            hint=item.hint,
        ))
        order += 1

    # Translate: full sentence production
    if sentences:
        sent = sentences[0]
        exercises.append(build_translate(
            ex_id=f"{ex_id_prefix}_tr_1",
            order_index=order,
            prompt=f"Translate: '{sent.source}'",
            source_text=sent.source,
            correct_answer=sent.target,
            accepted_answers=[sent.target],
        ))
        order += 1

    # Word bank
    if len(sentences) >= 2:
        sent = sentences[1]
        words = sent.words or sent.target.split()
        distractors_wb = [v.target for v in vocab if v.target not in words][:2]
        exercises.append(build_word_bank(
            ex_id=f"{ex_id_prefix}_wb_1",
            order_index=order,
            prompt=f"Translate to target language: '{sent.source}'",
            correct_answer=sent.target,
            words=words + distractors_wb,
        ))
        order += 1

    # Match pairs: all vocab
    if len(vocab) >= 3:
        pairs = [{"left": v.source, "right": v.target} for v in vocab[:4]]
        exercises.append(build_match_pairs(
            ex_id=f"{ex_id_prefix}_mp_1",
            order_index=order,
            prompt="Match all the words:",
            pairs=pairs,
        ))
        order += 1

    # Fill blank: final mastery check
    if sentences and sentences[0].blank_word:
        sent = sentences[0]
        exercises.append(build_fill_blank(
            ex_id=f"{ex_id_prefix}_fb_1",
            order_index=order,
            prompt="Fill in the blank:",
            correct_answer=sent.blank_word,
            sentence_before=sent.blank_before or "",
            sentence_after=sent.blank_after or "",
        ))
        order += 1

    return exercises
