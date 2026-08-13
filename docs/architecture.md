# Duolingo Platform Architecture Documentation

High-level architecture, domain boundaries, database schemas, and state flows.

---

## 1. Domain Module Architecture

```text
backend/app/modules/
├── user/          --> Learner identity & aggregated profile BFF endpoint
├── course/        --> Course catalog & unit hierarchy
├── lesson/        --> Lesson sessions, exercise registry, & answer validation engine
├── progress/      --> Central progression single source of truth & skill status calculation
├── gamification/  --> XP, streaks, daily goals, achievements, & heart regeneration
├── leaderboard/   --> Standard competition ranking (1224 rank) & standings
```

---

## 2. Core State Flows

### Answer Validation & Heart Flow
```text
Exercise UI -> POST /lessons/{id}/exercises/{exercise_id}/answer
            -> Refresh Hearts (Lazy Time Regen)
            -> Validate Answer (Strategy Pattern)
            -> Record ExerciseAttempt
            -> If Incorrect: Deduct Heart
            -> Return Response
```

### Lesson Completion Flow
```text
POST /lessons/{id}/complete
 -> Record Completed Attempt
 -> Award Lesson XP (UserStats)
 -> Update Streak & Daily Goal (DailyActivity)
 -> Upsert SkillProgress & Trigger Unlock Cascade
 -> Evaluate Achievements (Data-driven rules)
 -> COMMIT Transaction
 -> Return Rewards & newly_earned Achievements
```

---

## 3. Database Models

- `users` (1-to-1) `user_stats`
- `courses` -> `units` -> `skills` -> `lessons` -> `exercises`
- `lesson_attempts` -> `exercise_attempts`
- `skill_progress`
- `daily_activities`
- `achievements` -> `user_achievements`
- `leaderboard_entries`
