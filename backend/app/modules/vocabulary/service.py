import json
from typing import List, Optional, Dict, Any, Set
from sqlalchemy.orm import Session, joinedload
from app.modules.course.models import CourseModel, UnitModel
from app.modules.lesson.models import SkillModel, LessonModel, ExerciseModel
from app.modules.vocabulary.schemas import VocabularyResponse, VocabularyItem
from app.shared.errors import NotFoundError

# Core curriculum topic vocabulary dictionary
VOCAB_DICTIONARY: Dict[str, List[Dict[str, Any]]] = {
    "crs_english": [
        {"word": "Hello", "translation": "नमस्ते", "topic": "Greetings", "difficulty": 1, "phonetic": "/həˈloʊ/"},
        {"word": "Good morning", "translation": "शुभ प्रभात", "topic": "Greetings", "difficulty": 1, "phonetic": "/ɡʊd ˈmɔːrnɪŋ/"},
        {"word": "Thank you", "translation": "धन्यवाद", "topic": "Greetings", "difficulty": 1, "phonetic": "/θæŋk juː/"},
        {"word": "Goodbye", "translation": "अलविदा", "topic": "Greetings", "difficulty": 1, "phonetic": "/ɡʊdˈbaɪ/"},
        {"word": "Apple", "translation": "सेब", "topic": "Food", "difficulty": 1, "phonetic": "/ˈæp.əl/"},
        {"word": "Bread", "translation": "रोटी / ब्रेड", "topic": "Food", "difficulty": 1, "phonetic": "/bred/"},
        {"word": "Water", "translation": "पानी", "topic": "Food", "difficulty": 1, "phonetic": "/ˈwɑː.t̬ɚ/"},
        {"word": "Restaurant", "translation": "रेस्तरां", "topic": "Food", "difficulty": 2, "phonetic": "/ˈres.tə.rɑːnt/"},
        {"word": "Mother", "translation": "माँ", "topic": "Family", "difficulty": 1, "phonetic": "/ˈmʌð.ɚ/"},
        {"word": "Father", "translation": "पिता", "topic": "Family", "difficulty": 1, "phonetic": "/ˈfɑː.ðɚ/"},
        {"word": "Airport", "translation": "हवाई अड्डा", "topic": "Travel", "difficulty": 2, "phonetic": "/ˈer.pɔːrt/"},
        {"word": "Hotel", "translation": "होटल", "topic": "Travel", "difficulty": 1, "phonetic": "/hoʊˈtel/"},
        {"word": "Passport", "translation": "पासपोर्ट", "topic": "Travel", "difficulty": 2, "phonetic": "/ˈpæs.pɔːrt/"},
        {"word": "Ticket", "translation": "टिकट", "topic": "Travel", "difficulty": 1, "phonetic": "/ˈtɪk.ɪt/"},
    ],
    "crs_spanish": [
        {"word": "Hola", "translation": "Hello", "topic": "Greetings", "difficulty": 1, "phonetic": "/'o.la/"},
        {"word": "Buenos días", "translation": "Good morning", "topic": "Greetings", "difficulty": 1, "phonetic": "/'bwe.nos 'di.as/"},
        {"word": "Gracias", "translation": "Thank you", "topic": "Greetings", "difficulty": 1, "phonetic": "/'gɾa.sjas/"},
        {"word": "Adiós", "translation": "Goodbye", "topic": "Greetings", "difficulty": 1, "phonetic": "/a'ðjos/"},
        {"word": "Manzana", "translation": "Apple", "topic": "Food", "difficulty": 1, "phonetic": "/man'sa.na/"},
        {"word": "Agua", "translation": "Water", "topic": "Food", "difficulty": 1, "phonetic": "/'a.ɣwa/"},
        {"word": "Pan", "translation": "Bread", "topic": "Food", "difficulty": 1, "phonetic": "/pan/"},
        {"word": "Restaurante", "translation": "Restaurant", "topic": "Food", "difficulty": 2, "phonetic": "/res.tau'ran.te/"},
        {"word": "Aeropuerto", "translation": "Airport", "topic": "Travel", "difficulty": 2, "phonetic": "/a.e.ɾo'pweɾ.to/"},
        {"word": "Hotel", "translation": "Hotel", "topic": "Travel", "difficulty": 1, "phonetic": "/o'tel/"},
    ],
    "crs_french": [
        {"word": "Bonjour", "translation": "Hello / Good morning", "topic": "Greetings", "difficulty": 1, "phonetic": "/bɔ̃.ʒuʁ/"},
        {"word": "Merci", "translation": "Thank you", "topic": "Greetings", "difficulty": 1, "phonetic": "/mɛʁ.si/"},
        {"word": "Au revoir", "translation": "Goodbye", "topic": "Greetings", "difficulty": 1, "phonetic": "/o ʁə.vwaʁ/"},
        {"word": "Pomme", "translation": "Apple", "topic": "Food", "difficulty": 1, "phonetic": "/pɔm/"},
        {"word": "Eau", "translation": "Water", "topic": "Food", "difficulty": 1, "phonetic": "/o/"},
        {"word": "Pain", "translation": "Bread", "topic": "Food", "difficulty": 1, "phonetic": "/pɛ̃/"},
        {"word": "Restaurant", "translation": "Restaurant", "topic": "Food", "difficulty": 2, "phonetic": "/ʁɛs.to.ʁɑ̃/"},
        {"word": "Hôtel", "translation": "Hotel", "topic": "Travel", "difficulty": 1, "phonetic": "/o.tɛl/"},
    ],
}


class VocabularyService:
    """Service providing categorized course vocabulary exploration."""

    def __init__(self, db: Session):
        self.db = db

    def get_course_vocabulary(
        self,
        course_id: Optional[str] = None,
        topic: Optional[str] = None,
        difficulty: Optional[int] = None,
        query: Optional[str] = None,
    ) -> VocabularyResponse:
        c_id = course_id or "crs_english"
        course = self.db.query(CourseModel).filter_by(id=c_id).first()
        if not course:
            raise NotFoundError(f"Course '{c_id}' not found.")

        raw_vocab = VOCAB_DICTIONARY.get(c_id, VOCAB_DICTIONARY["crs_english"])
        all_topics = sorted(list({v["topic"] for v in raw_vocab}))

        items: List[VocabularyItem] = []
        for idx, v in enumerate(raw_vocab):
            # Apply filters
            if topic and topic.lower() != "all" and v["topic"].lower() != topic.lower():
                continue
            if difficulty and v["difficulty"] != difficulty:
                continue
            if query:
                q_clean = query.strip().lower()
                if q_clean not in v["word"].lower() and q_clean not in v["translation"].lower():
                    continue

            items.append(
                VocabularyItem(
                    id=f"vcb_{c_id}_{idx+1}",
                    word=v["word"],
                    translation=v["translation"],
                    topic=v["topic"],
                    difficulty=v["difficulty"],
                    course_id=course.id,
                    course_name=course.name,
                    skill_title=f"{v['topic']} Basics",
                    phonetic=v.get("phonetic"),
                )
            )

        return VocabularyResponse(
            course_id=course.id,
            total_items=len(items),
            topics=all_topics,
            items=items,
        )
