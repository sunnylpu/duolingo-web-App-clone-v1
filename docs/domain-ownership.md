# Domain Ownership & Event Architecture Specification

## 1. Domain Ownership Map

```text
User Domain
└── Identity, profile, avatar, preferences

Course Domain
└── Curriculum hierarchy (Course -> Unit -> Skill -> Lesson -> Exercise)

Lesson Domain
└── Active lesson sessions, exercise submission, attempt verification

Progress Domain
└── Skill progress, crown levels, unit milestones, course mastery

Gamification Domain
└── Total XP, heart regeneration, daily streaks, quests, achievements

Leaderboard Domain
└── Weekly rankings, XP aggregation

Social Domain
└── User follow graph, social activity feed

Notifications Domain
└── Notifications inbox, unread counts, automated reminder delivery

Ops Domain
└── Observability metrics, Prometheus counters, transactional audit logs
```

---

## 2. Event Flow Topology

```text
               Learner Submits Correct Answer
                            │
                            ▼
                    Lesson Domain
                   (ExerciseAttempt)
                            │
                            ▼
                    Progress Domain
                 (Check Lesson Finish)
                            │
              ┌─────────────┼─────────────┐
              ▼             ▼             ▼
        Gamification    Social         Audit
         (+XP, Quest)  (Activity)    (AuditEvent)
              │
              ▼
        Achievements
       (Unlock Event)
              │
              ▼
        Notifications
      (Push Notification)
```
