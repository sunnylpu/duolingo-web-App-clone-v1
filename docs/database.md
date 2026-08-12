# Duolingo Clone Database Documentation (Phase 02)

## Overview

The Duolingo Clone database layer utilizes **SQLAlchemy 2.0 ORM** with clean domain model separation across 6 backend modules (`user`, `course`, `lesson`, `progress`, `gamification`, `leaderboard`).

---

## Final Database Model Tree (14 Relational Models)

```
app/modules/
├── user/
│   └── models.py -> UserModel (`users`)
│
├── course/
│   └── models.py -> CourseModel (`courses`), UnitModel (`units`)
│
├── lesson/
│   └── models.py -> SkillModel (`skills`), LessonModel (`lessons`), ExerciseModel (`exercises`)
│
├── progress/
│   └── models.py -> SkillProgressModel (`skill_progress`), LessonAttemptModel (`lesson_attempts`), 
│                    ExerciseAttemptModel (`exercise_attempts`), DailyActivityModel (`daily_activities`)
│
├── gamification/
│   └── models.py -> UserStatsModel (`user_stats`), AchievementModel (`achievements`), 
│                    UserAchievementModel (`user_achievements`)
│
└── leaderboard/
    └── models.py -> LeaderboardEntryModel (`leaderboard_entries`)
```

---

## Entity Relationship Overview

### Content Hierarchy
$$\text{Course} \xrightarrow{\text{1:N}} \text{Unit} \xrightarrow{\text{1:N}} \text{Skill} \xrightarrow{\text{1:N}} \text{Lesson} \xrightarrow{\text{1:N}} \text{Exercise}$$

- **Course**: Language course entity (e.g. Spanish for English speakers).
- **Unit**: Thematic grouping of skills within a course (e.g. Unit 1: Greetings).
- **Skill**: Skill node within a unit. Supports prerequisite progression via self-referencing `prerequisite_skill_id`.
- **Lesson**: Individual learning module belonging to a skill.
- **Exercise**: Individual exercise question. Uses flexible `JSON` storage to support all 6 exercise types (`multiple_choice`, `translate`, `word_bank`, `match_pairs`, `fill_blank`, `type_answer`).

### User State & Progress Hierarchy
$$\text{User} \xrightarrow{\text{1:1}} \text{UserStats}$$
$$\text{User} \xrightarrow{\text{1:N}} \text{SkillProgress}$$
$$\text{User} \xrightarrow{\text{1:N}} \text{LessonAttempt} \xrightarrow{\text{1:N}} \text{ExerciseAttempt}$$
$$\text{User} \xrightarrow{\text{1:N}} \text{DailyActivity}$$
$$\text{User} \xrightarrow{\text{1:N}} \text{UserAchievement} \xleftarrow{\text{N:1}} \text{Achievement}$$
$$\text{User} \xrightarrow{\text{1:N}} \text{LeaderboardEntry}$$

---

## Data Integrity, Indexes & Constraints

### Primary & Foreign Key Cascades
- All child tables reference parents using `ForeignKey` with `ondelete="CASCADE"` (e.g. deleting a `Course` automatically cascades deletion to its `Unit`s, `Skill`s, `Lesson`s, and `Exercise`s).
- Self-referencing prerequisite links (`SkillModel.prerequisite_skill_id`) use `ondelete="SET NULL"`.

### Unique Constraints
- `UserStatsModel`: Unique index on `user_id` enforcing 1-to-1 relationship with `UserModel`.
- `SkillProgressModel`: `UniqueConstraint("user_id", "skill_id", name="uq_user_skill_progress")`
- `DailyActivityModel`: `UniqueConstraint("user_id", "activity_date", name="uq_user_daily_activity")`
- `UserAchievementModel`: `UniqueConstraint("user_id", "achievement_id", name="uq_user_achievement")`

### Indexes
- Foreign key columns (`user_id`, `course_id`, `unit_id`, `skill_id`, `lesson_id`, `exercise_id`, `achievement_id`).
- High-frequency query filters (`exercise_type`, `activity_date`, `leaderboard_period`, `user_username`, `user_email`).

---

## Database Initialization & Seed Script

### Initialize Database Schemas
Programmatically via Python:
```python
from app.shared.database import init_db
init_db()
```

### Run Idempotent Seed Script
Command line:
```bash
cd backend
python3 -m seed.seed
```

#### Seed Output Metrics:
- **1 Course**: Spanish (`es`)
- **3 Units**: Greetings, Food & Family, Directions & Travel
- **6 Skills**: Greetings, Basics, Food, Family, Directions, Travel Basics
- **8 Lessons**: 1-2 per skill
- **13 Exercises**: Covering `multiple_choice`, `translate`, `word_bank`, `match_pairs`, `fill_blank`, `type_answer`
- **4 Users**: 1 Demo Learner (`usr_demo`) and 3 Leaderboard Users
- **4 Achievements**: `FIRST_LESSON`, `100_XP`, `500_XP`, `7_DAY_STREAK`
- **4 Leaderboard Entries**: Weekly standings

---

## Microservices Extraction Strategy

Because database models are strictly partitioned by domain modules and use explicit foreign keys, extracting a domain like `lesson` or `user` into a microservice involves:
1. Extracting `app/modules/lesson/` into `lesson-service/`.
2. Migrating `skills`, `lessons`, and `exercises` tables to a dedicated database instance.
3. Replacing cross-domain foreign key joins with RPC/REST client references.
