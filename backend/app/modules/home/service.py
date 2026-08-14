from typing import Optional, List
from sqlalchemy.orm import Session, joinedload
from app.modules.progress.service import ProgressService
from app.modules.gamification.service import GamificationService
from app.modules.course.service import CourseService
from app.modules.course.models import UnitModel
from app.modules.lesson.models import SkillModel, LessonModel
from app.modules.user.models import UserModel
from app.modules.home.schemas import (
    HomeDashboardResponse,
    ContinueLearningSummary,
    HomeDailyGoalSummary,
    HomeStreakSummary,
    HomeHeartsSummary,
    HomeReviewSummary,
)

MAX_HEARTS = 5


class HomeService:
    """
    BFF-style aggregation domain service for the Learner Dashboard.
    Composes ProgressService, GamificationService, CourseService, and UserService.
    """

    def __init__(self, db: Session):
        self.db = db
        self.progress_service = ProgressService(db)
        self.gamification_service = GamificationService(db)
        self.course_service = CourseService(db)

    def get_home_dashboard(
        self, current_user: UserModel, course_id: Optional[str] = None
    ) -> HomeDashboardResponse:
        # Fetch course-aware path (also calculates stats & recommendations)
        path = self.progress_service.get_learning_path(current_user=current_user, course_id=course_id)
        current_course = path.course

        # Fetch continue learning details
        rec_skill_id = path.recommended_skill_id
        rec_lesson_id = path.recommended_lesson_id
        rec_unit_id = path.recommended_unit_id

        continue_learning = ContinueLearningSummary()

        if rec_unit_id and rec_skill_id:
            unit_obj = self.db.query(UnitModel).filter_by(id=rec_unit_id).first()
            skill_obj = (
                self.db.query(SkillModel)
                .options(joinedload(SkillModel.lessons))
                .filter_by(id=rec_skill_id)
                .first()
            )
            lesson_obj = (
                self.db.query(LessonModel).filter_by(id=rec_lesson_id).first()
                if rec_lesson_id
                else None
            )

            if unit_obj and skill_obj:
                state = self.progress_service.evaluate_skill_state(current_user.id, skill_obj)
                continue_learning = ContinueLearningSummary(
                    unit_id=unit_obj.id,
                    unit_title=f"Unit {unit_obj.order_index} · {unit_obj.title}",
                    skill_id=skill_obj.id,
                    skill_title=skill_obj.title,
                    lesson_id=lesson_obj.id if lesson_obj else (skill_obj.lessons[0].id if skill_obj.lessons else None),
                    lesson_title=lesson_obj.title if lesson_obj else "Start Lesson",
                    progress_percent=state.get("completion_percent", 0.0),
                    lessons_completed=state.get("lessons_completed", 0),
                    total_lessons=state.get("total_lessons", len(skill_obj.lessons)),
                )

        # Fetch gamification stats (heart refresh, streak, daily goal)
        stats = self.gamification_service.refresh_hearts(current_user.id)
        daily_goal = HomeDailyGoalSummary(
            xp=stats.daily_xp or 0,
            goal=stats.daily_goal_xp or 30,
            goal_completed=bool((stats.daily_xp or 0) >= (stats.daily_goal_xp or 30)),
            goal_just_completed=False,
        )
        streak = HomeStreakSummary(
            current_streak=stats.current_streak or 0,
            longest_streak=stats.longest_streak or 0,
            is_active_today=bool(stats.daily_xp and stats.daily_xp > 0),
        )
        hearts = HomeHeartsSummary(
            hearts=stats.hearts if stats.hearts is not None else MAX_HEARTS,
            max_hearts=MAX_HEARTS,
            next_heart_refill_seconds=None,
        )

        # Fetch smart review summary
        review_data = self.progress_service.get_smart_review(
            current_user=current_user, course_id=current_course.id
        )
        smart_review = HomeReviewSummary(
            available=review_data.available,
            count=review_data.count,
            skills_count=len(review_data.skills),
        )

        # Fetch all courses with progress
        courses = self.course_service.get_courses(current_user=current_user)

        return HomeDashboardResponse(
            course=current_course,
            continue_learning=continue_learning,
            daily_goal=daily_goal,
            streak=streak,
            hearts=hearts,
            smart_review=smart_review,
            courses=courses,
        )
