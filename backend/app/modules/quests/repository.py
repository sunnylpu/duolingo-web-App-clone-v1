import datetime
from typing import List, Optional
from sqlalchemy.orm import Session, joinedload
from app.modules.quests.models import QuestModel, UserQuestModel


class QuestRepository:
    """Database persistence repository for Quests and UserQuests."""

    def __init__(self, db: Session):
        self.db = db

    def get_or_create_quest(
        self,
        quest_id: str,
        code: str,
        title: str,
        description: str,
        quest_type: str,
        target_value: int,
        reward_xp: int = 20,
        quest_scope: str = "daily",
        course_id: Optional[str] = None,
    ) -> QuestModel:
        existing = self.db.query(QuestModel).filter_by(code=code).first()
        if existing:
            return existing

        quest = QuestModel(
            id=quest_id,
            code=code,
            title=title,
            description=description,
            quest_type=quest_type,
            target_value=target_value,
            reward_xp=reward_xp,
            quest_scope=quest_scope,
            course_id=course_id,
        )
        self.db.add(quest)
        self.db.flush()
        return quest

    def get_user_quests_for_date(self, user_id: str, ref_date: datetime.date) -> List[UserQuestModel]:
        return (
            self.db.query(UserQuestModel)
            .options(joinedload(UserQuestModel.quest))
            .join(QuestModel, UserQuestModel.quest_id == QuestModel.id)
            .filter(
                UserQuestModel.user_id == user_id,
                UserQuestModel.reference_date == ref_date,
                QuestModel.quest_scope == "daily",
            )
            .all()
        )

    def get_user_weekly_quest(self, user_id: str, week_start_date: datetime.date) -> Optional[UserQuestModel]:
        return (
            self.db.query(UserQuestModel)
            .options(joinedload(UserQuestModel.quest))
            .join(QuestModel, UserQuestModel.quest_id == QuestModel.id)
            .filter(
                UserQuestModel.user_id == user_id,
                UserQuestModel.reference_date == week_start_date,
                QuestModel.quest_scope == "weekly",
            )
            .first()
        )

    def assign_user_quest(
        self, user_quest_id: str, user_id: str, quest_id: str, ref_date: datetime.date
    ) -> UserQuestModel:
        existing = (
            self.db.query(UserQuestModel)
            .filter_by(user_id=user_id, quest_id=quest_id, reference_date=ref_date)
            .first()
        )
        if existing:
            return existing

        user_quest = UserQuestModel(
            id=user_quest_id,
            user_id=user_id,
            quest_id=quest_id,
            current_value=0,
            completed=False,
            reference_date=ref_date,
        )
        self.db.add(user_quest)
        self.db.flush()
        return user_quest

    def get_active_user_quests_by_type(
        self, user_id: str, quest_type: str, ref_date: datetime.date
    ) -> List[UserQuestModel]:
        return (
            self.db.query(UserQuestModel)
            .options(joinedload(UserQuestModel.quest))
            .join(QuestModel, UserQuestModel.quest_id == QuestModel.id)
            .filter(
                UserQuestModel.user_id == user_id,
                UserQuestModel.completed == False,
                UserQuestModel.reference_date == ref_date,
                QuestModel.quest_type == quest_type,
            )
            .all()
        )

    def get_user_completed_quests_history(self, user_id: str, limit: int = 20) -> List[UserQuestModel]:
        return (
            self.db.query(UserQuestModel)
            .options(joinedload(UserQuestModel.quest))
            .filter(UserQuestModel.user_id == user_id, UserQuestModel.completed == True)
            .order_by(UserQuestModel.completed_at.desc())
            .limit(limit)
            .all()
        )
