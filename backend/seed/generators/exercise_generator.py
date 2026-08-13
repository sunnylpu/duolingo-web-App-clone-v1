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
    others = [w for w in pool if w.lower().strip() != correct.lower().strip()]
    selected = others[:n]
    # Fallback to sensible defaults if vocabulary pool is small
    default_fillers = ["Option A", "Option B", "Option C", "Option D"]
    idx = 0
    while len(selected) < n:
        filler = default_fillers[idx % len(default_fillers)]
        if filler != correct and filler not in selected:
            selected.append(filler)
        idx += 1
    return selected


# ── Individual exercise builders (using ex_id deterministic seeding) ──────────────

def build_multiple_choice(
    ex_id: str,
    order_index: int,
    prompt: str,
    correct_answer: str,
    options: List[str],
    xp_reward: int = 5,
) -> Dict[str, Any]:
    """Multiple-choice question with 4 options (correct + 3 distractors)."""
    rng = random.Random(ex_id)
    opts = [correct_answer]
    for opt in options:
        if opt not in opts:
            opts.append(opt)
        if len(opts) == 4:
            break
    while len(opts) < 4:
        filler = f"Choice {len(opts)+1}"
        if filler not in opts:
            opts.append(filler)
    rng.shuffle(opts)
    return {
        "id": ex_id,
        "type": "multiple_choice",
        "prompt": prompt,
        "correct_answer": correct_answer,
        "data": {"options": opts},
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
    acc = accepted_answers or [correct_answer]
    if correct_answer not in acc:
        acc.append(correct_answer)
    return {
        "id": ex_id,
        "type": "translate",
        "prompt": prompt,
        "correct_answer": correct_answer,
        "data": {
            "source_text": source_text,
            "accepted_answers": acc,
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
    rng = random.Random(ex_id)
    shuffled = list(words)
    rng.shuffle(shuffled)
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


# ── High-level: generate exactly 6 exercises per lesson with varied sequences ────────────────

def generate_learn_exercises(
    skill: SkillSpec,
    lesson_id_prefix: str,
    ex_id_prefix: str,
    target_lang_label: str = "English",
) -> List[Dict[str, Any]]:
    """
    Lesson 1 — Learn: Recognition and introduction.
    Sequence: MCQ -> Translate -> Word Bank -> Fill Blank -> Type Answer -> MCQ
    Guarantees exactly 6 exercises per lesson.
    """
    vocab = skill.vocabulary
    sentences = skill.sentences
    all_targets = [v.target for v in vocab]
    all_sources = [v.source for v in vocab]

    v0 = vocab[0] if len(vocab) > 0 else VocabItem("Hello", "नमस्ते")
    v1 = vocab[1] if len(vocab) > 1 else v0
    v2 = vocab[2] if len(vocab) > 2 else v0
    s0 = sentences[0] if len(sentences) > 0 else SentenceItem(v0.target, v0.source, v0.target.split())
    s1 = sentences[1] if len(sentences) > 1 else s0

    exercises = []

    # 1. Multiple Choice: Target word recognition
    exercises.append(build_multiple_choice(
        ex_id=f"{ex_id_prefix}_1",
        order_index=1,
        prompt=f"What does '{v0.source}' mean in {target_lang_label}?",
        correct_answer=v0.target,
        options=_distractors(v0.target, all_targets, 3),
    ))

    # 2. Translate: Sentence translation
    exercises.append(build_translate(
        ex_id=f"{ex_id_prefix}_2",
        order_index=2,
        prompt=f"Translate: '{s0.source}'",
        source_text=s0.source,
        correct_answer=s0.target,
        accepted_answers=[s0.target, s0.target.strip(".")],
    ))

    # 3. Word Bank: Sentence construction
    words0 = s0.words or s0.target.split()
    distractors_wb = [v.target for v in vocab if v.target not in words0][:2]
    exercises.append(build_word_bank(
        ex_id=f"{ex_id_prefix}_3",
        order_index=3,
        prompt=f"Build in {target_lang_label}: '{s0.source}'",
        correct_answer=s0.target,
        words=words0 + distractors_wb,
    ))

    # 4. Fill in the Blank
    blank_word = s0.blank_word or (s0.target.split()[-1] if s0.target.split() else v0.target)
    before_text = s0.blank_before or (" ".join(s0.target.split()[:-1]) if len(s0.target.split()) > 1 else "")
    after_text = s0.blank_after or ""
    exercises.append(build_fill_blank(
        ex_id=f"{ex_id_prefix}_4",
        order_index=4,
        prompt="Complete the sentence:",
        correct_answer=blank_word,
        sentence_before=before_text,
        sentence_after=after_text,
        options=_distractors(blank_word, all_targets, 3),
    ))

    # 5. Type Answer: Target word production
    exercises.append(build_type_answer(
        ex_id=f"{ex_id_prefix}_5",
        order_index=5,
        prompt=f"Type in {target_lang_label}: '{v1.source}'",
        correct_answer=v1.target,
        hint=v1.hint,
    ))

    # 6. Multiple Choice: Reverse meaning recognition
    exercises.append(build_multiple_choice(
        ex_id=f"{ex_id_prefix}_6",
        order_index=6,
        prompt=f"What does '{v2.target}' mean?",
        correct_answer=v2.source,
        options=_distractors(v2.source, all_sources, 3),
    ))

    return exercises


def generate_practice_exercises(
    skill: SkillSpec,
    lesson_id_prefix: str,
    ex_id_prefix: str,
    source_lang_label: str = "English",
) -> List[Dict[str, Any]]:
    """
    Lesson 2 — Practice: Application and sentence structure.
    Sequence: Word Bank -> Match Pairs -> Translate -> MCQ -> Fill Blank -> Type Answer
    Guarantees exactly 6 exercises per lesson.
    """
    vocab = skill.vocabulary
    sentences = skill.sentences
    all_targets = [v.target for v in vocab]
    all_sources = [v.source for v in vocab]

    v0 = vocab[0] if len(vocab) > 0 else VocabItem("Hello", "नमस्ते")
    v1 = vocab[1] if len(vocab) > 1 else v0
    v2 = vocab[2] if len(vocab) > 2 else v0
    s0 = sentences[0] if len(sentences) > 0 else SentenceItem(v0.target, v0.source, v0.target.split())
    s1 = sentences[1] if len(sentences) > 1 else s0

    exercises = []

    # 1. Word Bank: Build sentence
    words1 = s1.words or s1.target.split()
    distractors_wb = [v.target for v in vocab if v.target not in words1][:2]
    exercises.append(build_word_bank(
        ex_id=f"{ex_id_prefix}_1",
        order_index=1,
        prompt=f"Translate: '{s1.source}'",
        correct_answer=s1.target,
        words=words1 + distractors_wb,
    ))

    # 2. Match Pairs: Vocabulary matching
    pairs_list = [{"left": item.source, "right": item.target} for item in vocab[:3]]
    if len(pairs_list) < 3:
        pairs_list.append({"left": v0.source, "right": v0.target})
    exercises.append(build_match_pairs(
        ex_id=f"{ex_id_prefix}_2",
        order_index=2,
        prompt="Match the vocabulary pairs:",
        pairs=pairs_list,
    ))

    # 3. Translate: Full sentence translation
    exercises.append(build_translate(
        ex_id=f"{ex_id_prefix}_3",
        order_index=3,
        prompt=f"Translate to target language: '{s1.source}'",
        source_text=s1.source,
        correct_answer=s1.target,
        accepted_answers=[s1.target, s1.target.strip(".")],
    ))

    # 4. Multiple Choice: Context check
    exercises.append(build_multiple_choice(
        ex_id=f"{ex_id_prefix}_4",
        order_index=4,
        prompt=f"Which phrase translates to '{v1.source}'?",
        correct_answer=v1.target,
        options=_distractors(v1.target, all_targets, 3),
    ))

    # 5. Fill Blank: Grammatical completion
    blank_word = s1.blank_word or (s1.target.split()[0] if s1.target.split() else v1.target)
    before_text = s1.blank_before or ""
    after_text = s1.blank_after or (" ".join(s1.target.split()[1:]) if len(s1.target.split()) > 1 else "")
    exercises.append(build_fill_blank(
        ex_id=f"{ex_id_prefix}_5",
        order_index=5,
        prompt="Fill in the missing word:",
        correct_answer=blank_word,
        sentence_before=before_text,
        sentence_after=after_text,
        options=_distractors(blank_word, all_targets, 3),
    ))

    # 6. Type Answer: Practice spelling/typing
    exercises.append(build_type_answer(
        ex_id=f"{ex_id_prefix}_6",
        order_index=6,
        prompt=f"Type in target language: '{v2.source}'",
        correct_answer=v2.target,
        hint=v2.hint,
    ))

    return exercises


def generate_mastery_exercises(
    skill: SkillSpec,
    lesson_id_prefix: str,
    ex_id_prefix: str,
    target_lang_label: str = "English",
) -> List[Dict[str, Any]]:
    """
    Lesson 3 — Mastery: Independent production and full comprehension check.
    Sequence: Translate -> Type Answer -> Match Pairs -> Word Bank -> Fill Blank -> MCQ
    Guarantees exactly 6 exercises per lesson.
    """
    vocab = skill.vocabulary
    sentences = skill.sentences
    all_targets = [v.target for v in vocab]
    all_sources = [v.source for v in vocab]

    v0 = vocab[0] if len(vocab) > 0 else VocabItem("Hello", "नमस्ते")
    v1 = vocab[1] if len(vocab) > 1 else v0
    v2 = vocab[-1] if len(vocab) > 0 else v0
    s0 = sentences[0] if len(sentences) > 0 else SentenceItem(v0.target, v0.source, v0.target.split())
    s2 = sentences[-1] if len(sentences) > 0 else s0

    exercises = []

    # 1. Translate: Complex sentence translation
    exercises.append(build_translate(
        ex_id=f"{ex_id_prefix}_1",
        order_index=1,
        prompt=f"Translate: '{s2.source}'",
        source_text=s2.source,
        correct_answer=s2.target,
        accepted_answers=[s2.target, s2.target.strip(".")],
    ))

    # 2. Type Answer: Free production
    exercises.append(build_type_answer(
        ex_id=f"{ex_id_prefix}_2",
        order_index=2,
        prompt=f"Type in {target_lang_label}: '{v2.source}'",
        correct_answer=v2.target,
        hint=v2.hint,
    ))

    # 3. Match Pairs: Comprehensive vocabulary check
    pairs_list = [{"left": item.source, "right": item.target} for item in vocab[-3:]]
    if len(pairs_list) < 3:
        pairs_list = [{"left": item.source, "right": item.target} for item in vocab[:3]]
    exercises.append(build_match_pairs(
        ex_id=f"{ex_id_prefix}_3",
        order_index=3,
        prompt="Match all words correctly:",
        pairs=pairs_list,
    ))

    # 4. Word Bank: Complex sentence construction
    words2 = s2.words or s2.target.split()
    distractors_wb = [v.target for v in vocab if v.target not in words2][:2]
    exercises.append(build_word_bank(
        ex_id=f"{ex_id_prefix}_4",
        order_index=4,
        prompt=f"Construct sentence for: '{s2.source}'",
        correct_answer=s2.target,
        words=words2 + distractors_wb,
    ))

    # 5. Fill Blank: Advanced blank completion
    blank_word = s2.blank_word or (s2.target.split()[-1] if s2.target.split() else v2.target)
    before_text = s2.blank_before or (" ".join(s2.target.split()[:-1]) if len(s2.target.split()) > 1 else "")
    after_text = s2.blank_after or ""
    exercises.append(build_fill_blank(
        ex_id=f"{ex_id_prefix}_5",
        order_index=5,
        prompt="Fill in the blank for mastery:",
        correct_answer=blank_word,
        sentence_before=before_text,
        sentence_after=after_text,
        options=_distractors(blank_word, all_targets, 3),
    ))

    # 6. Multiple Choice: Final mastery prompt
    exercises.append(build_multiple_choice(
        ex_id=f"{ex_id_prefix}_6",
        order_index=6,
        prompt=f"What is the correct translation for '{v2.source}'?",
        correct_answer=v2.target,
        options=_distractors(v2.target, all_targets, 3),
    ))

    return exercises
