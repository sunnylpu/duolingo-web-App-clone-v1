import hashlib
import datetime
from typing import List, Optional
from sqlalchemy.orm import Session
from app.modules.quests.repository import QuestRepository
from app.modules.quests.schemas import (
    QuestItemResponse,
    DailyQuestsResponse,
    WeeklyChallengeResponse,
    QuestHistoryResponse,
)
from app.modules.user.models import UserModel
from app.modules.gamification.models import UserStatsModel
from app.modules.gamification.service import get_current_activity_date
from app.modules.progress.repository import ProgressRepository

DEFAULT_QUEST_TEMPLATES = [
    {
        "id": "qst_tpl_lessons_2",
        "code": "DAILY_LESSONS_2",
        "title": "Complete 2 lessons",
        "description": "Complete 2 lessons today to build your streak",
        "quest_type": "LESSONS_COMPLETED",
        "target_value": 2,
        "reward_xp": 20,
        "quest_scope": "daily",
    },
    {
        "id": "qst_tpl_xp_30",
        "code": "DAILY_XP_30",
        "title": "Earn 30 XP",
        "description": "Score 30 XP from lessons, reviews, or practice",
        "quest_type": "XP_EARNED",
        "target_value": 30,
        "reward_xp": 15,
        "quest_scope": "daily",
    },
    {
        "id": "qst_tpl_answers_10",
        "code": "DAILY_ANSWERS_10",
        "title": "Answer 10 correctly",
        "description": "Get 10 exercise questions right today",
        "quest_type": "CORRECT_ANSWERS",
        "target_value": 10,
        "reward_xp": 20,
        "quest_scope": "daily",
    },
    {
        "id": "qst_tpl_skill_1",
        "code": "DAILY_SKILL_1",
        "title": "Master 1 skill",
        "description": "Complete all lessons in any skill today",
        "quest_type": "SKILLS_COMPLETED",
        "target_value": 1,
        "reward_xp": 25,
        "quest_scope": "daily",
    },
    {
        "id": "qst_tpl_reviews_3",
        "code": "DAILY_REVIEWS_3",
        "title": "Complete 3 reviews",
        "description": "Practice weak items in Smart Review",
        "quest_type": "REVIEWS_COMPLETED",
        "target_value": 3,
        "reward_xp": 15,
        "quest_scope": "daily",
    },
    {
        "id": "qst_tpl_weekly_lessons_10",
        "code": "WEEKLY_LESSONS_10",
        "title": "Weekly Challenge: Complete 10 lessons",
        "description": "Complete 10 total lessons this week for a massive XP boost",
        "quest_type": "LESSONS_COMPLETED",
        "target_value": 10,
        "reward_xp": 100,
        "quest_scope": "weekly",
    },
]


class QuestService:
    """Service handling daily quest assignment, progress tracking, and reward settlement."""

    def __init__(self, db: Session):
        self.db = db
        self.repository = QuestRepository(db)
        self.progress_repository = ProgressRepository(db)
        self._ensure_default_quest_templates()

    def _ensure_default_quest_templates(self) -> None:
        for tpl in DEFAULT_QUEST_TEMPLATES:
            self.repository.get_or_create_quest(
                quest_id=tpl["id"],
                code=tpl["code"],
                title=tpl["title"],
                description=tpl["description"],
                quest_type=tpl["quest_type"],
                target_value=tpl["target_value"],
                reward_xp=tpl["reward_xp"],
                quest_scope=tpl["quest_scope"],
            )

    def get_today_quests(self, current_user: UserModel) -> DailyQuestsResponse:
        today = get_current_activity_date()
        user_quests = self.repository.get_user_quests_for_date(current_user.id, today)

        if len(user_quests) < 3:
            daily_templates = [t for t in DEFAULT_QUEST_TEMPLATES if t["quest_scope"] == "daily"]
            seed_str = f"{current_user.id}_{today.isoformat()}"
            hash_val = int(hashlib.md5(seed_str.encode("utf-8")).hexdigest(), 16)

            selected_templates = []
            num_templates = len(daily_templates)
            for i in range(3):
                idx = (hash_val + i * 7) % num_templates
                selected_templates.append(daily_templates[idx])

            seen_ids = set()
            unique_templates = []
            for tpl in selected_templates:
                if tpl["id"] not in seen_ids:
                    seen_ids.add(tpl["id"])
                    unique_templates.append(tpl)

            for idx, tpl in enumerate(unique_templates):
                uq_id = f"uq_{current_user.id}_{today.isoformat()}_{tpl['code']}"
                self.repository.assign_user_quest(
                    user_quest_id=uq_id,
                    user_id=current_user.id,
                    quest_id=tpl["id"],
                    ref_date=today,
                )

            self.db.commit()
            user_quests = self.repository.get_user_quests_for_date(current_user.id, today)

        items = [
            QuestItemResponse(
                id=uq.id,
                code=uq.quest.code,
                title=uq.quest.title,
                description=uq.quest.description,
                quest_type=uq.quest.quest_type,
                quest_scope=uq.quest.quest_scope,
                current_value=uq.current_value,
                target_value=uq.quest.target_value,
                reward_xp=uq.quest.reward_xp,
                completed=uq.completed,
                completed_at=uq.completed_at,
                course_id=uq.quest.course_id,
            )
            for uq in user_quests
        ]

        return DailyQuestsResponse(
            date=today.isoformat(),
            user_id=current_user.id,
            quests=items,
        )

    def get_weekly_challenge(self, current_user: UserModel) -> WeeklyChallengeResponse:
        today = get_current_activity_date()
        week_start = today - datetime.timedelta(days=today.weekday())

        user_quest = self.repository.get_user_weekly_quest(current_user.id, week_start)
        if not user_quest:
            weekly_tpl = DEFAULT_QUEST_TEMPLATES[-1]
            uq_id = f"uq_{current_user.id}_{week_start.isoformat()}_{weekly_tpl['code']}"
            user_quest = self.repository.assign_user_quest(
                user_quest_id=uq_id,
                user_id=current_user.id,
                quest_id=weekly_tpl["id"],
                ref_date=week_start,
            )
            self.db.commit()

        challenge = QuestItemResponse(
            id=user_quest.id,
            code=user_quest.quest.code,
            title=user_quest.quest.title,
            description=user_quest.quest.description,
            quest_type=user_quest.quest.quest_type,
            quest_scope=user_quest.quest.quest_scope,
            current_value=user_quest.current_value,
            target_value=user_quest.quest.target_value,
            reward_xp=user_quest.quest.reward_xp,
            completed=user_quest.completed,
            completed_at=user_quest.completed_at,
            course_id=user_quest.quest.course_id,
        )

        return WeeklyChallengeResponse(
            week_start_date=week_start.isoformat(),
            challenge=challenge,
        )

    def record_quest_event(
        self, user_id: str, quest_type: str, amount: int = 1, course_id: Optional[str] = None
    ) -> List[str]:
        today = get_current_activity_date()
        week_start = today - datetime.timedelta(days=today.weekday())

        user_obj = self.db.query(UserModel).filter_by(id=user_id).first()
        if not user_obj:
            return []

        self.get_today_quests(user_obj)
        self.get_weekly_challenge(user_obj)

        active_daily = self.repository.get_active_user_quests_by_type(user_id, quest_type, ref_date=today)
        active_weekly = self.repository.get_active_user_quests_by_type(user_id, quest_type, ref_date=week_start)

        active_user_quests = active_daily + active_weekly
        completed_titles: List[str] = []

        for uq in active_user_quests:
            if uq.completed:
                continue

            uq.current_value += amount
            if uq.current_value >= uq.quest.target_value:
                uq.completed = True
                uq.completed_at = datetime.datetime.utcnow()
                completed_titles.append(uq.quest.title)

                stats = self.db.query(UserStatsModel).filter_by(user_id=user_id).first()
                if stats:
                    stats.total_xp += uq.quest.reward_xp

                self.progress_repository.record_daily_activity(
                    activity_id=f"act_qxp_{user_id}_{uq.id}",
                    user_id=user_id,
                    activity_date=today,
                    xp_earned=uq.quest.reward_xp,
                    lessons_completed=0,
                    minutes_learned=0,
                )

        self.db.flush()
        return completed_titles

    def get_quest_history(self, current_user: UserModel, limit: int = 20) -> QuestHistoryResponse:
        history = self.repository.get_user_completed_quests_history(current_user.id, limit=limit)
        items = [
            QuestItemResponse(
                id=uq.id,
                code=uq.quest.code,
                title=uq.quest.title,
                description=uq.quest.description,
                quest_type=uq.quest.quest_type,
                quest_scope=uq.quest.quest_scope,
                current_value=uq.current_value,
                target_value=uq.quest.target_value,
                reward_xp=uq.quest.reward_xp,
                completed=uq.completed,
                completed_at=uq.completed_at,
                course_id=uq.quest.course_id,
            )
            for uq in history
        ]
        return QuestHistoryResponse(total_completed=len(items), quests=items)
