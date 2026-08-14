"""
Integration tests for Phase 28 — Social Layer: Friends, Following & Activity Feed.

Verifies:
1. Follow & unfollow endpoints & DB idempotency
2. Self-follow rejection validation
3. Followers & Following API responses
4. Friend suggestions API
5. Social activity feed recording & fetching
6. Public profile API (non-sensitive fields)
7. Friends leaderboard scope filtering (scope=friends)
"""

import pytest
from sqlalchemy.orm import Session
from app.modules.user.models import UserModel
from app.modules.social.service import SocialService
from app.modules.leaderboard.service import LeaderboardService
from app.shared.errors import ValidationError
from seed.seed import seed_database


@pytest.fixture()
def seeded_db(db_session: Session):
    seed_database(db_session)
    return db_session


def test_follow_and_unfollow_flow(seeded_db: Session):
    user_demo = seeded_db.query(UserModel).filter_by(id="usr_demo").first()
    user_spanish = seeded_db.query(UserModel).filter_by(id="usr_spanish_pro").first()
    service = SocialService(seeded_db)

    # Initial state: demo user follows polyglot and language_lover, but not spanish_pro
    assert service.repository.is_following(user_demo.id, user_spanish.id) is False

    # Follow spanish_pro
    service.follow_user(user_demo, user_spanish.id)
    assert service.repository.is_following(user_demo.id, user_spanish.id) is True

    # Duplicate follow safety
    service.follow_user(user_demo, user_spanish.id)
    assert service.repository.is_following(user_demo.id, user_spanish.id) is True

    # Unfollow spanish_pro
    service.unfollow_user(user_demo, user_spanish.id)
    assert service.repository.is_following(user_demo.id, user_spanish.id) is False


def test_self_follow_prevention(seeded_db: Session):
    user_demo = seeded_db.query(UserModel).filter_by(id="usr_demo").first()
    service = SocialService(seeded_db)

    with pytest.raises(ValidationError):
        service.follow_user(user_demo, user_demo.id)


def test_followers_and_following_queries(seeded_db: Session):
    user_demo = seeded_db.query(UserModel).filter_by(id="usr_demo").first()
    service = SocialService(seeded_db)

    following = service.get_following(user_demo)
    assert len(following) >= 2

    followers = service.get_followers(user_demo)
    assert len(followers) >= 1


def test_friend_suggestions(seeded_db: Session):
    user_demo = seeded_db.query(UserModel).filter_by(id="usr_demo").first()
    service = SocialService(seeded_db)

    suggestions = service.get_suggestions(user_demo)
    assert isinstance(suggestions, list)
    for item in suggestions:
        assert item.user.id != user_demo.id
        assert item.user.is_following is False


def test_activity_feed_recording_and_fetching(seeded_db: Session):
    user_demo = seeded_db.query(UserModel).filter_by(id="usr_demo").first()
    service = SocialService(seeded_db)

    service.record_activity_event(
        user_id=user_demo.id,
        event_type="skill_completed",
        message="mastered skill Greetings! 🔮",
        metadata={"skill_title": "Greetings"},
    )

    feed = service.get_activity_feed(user_demo, limit=10, offset=0)
    assert feed.total >= 1
    assert len(feed.items) > 0
    assert feed.items[0].message is not None


def test_public_profile_endpoint(seeded_db: Session):
    user_demo = seeded_db.query(UserModel).filter_by(id="usr_demo").first()
    service = SocialService(seeded_db)

    pub_prof = service.get_public_profile(user_demo, target_user_id="usr_polyglot")
    assert pub_prof.id == "usr_polyglot"
    assert pub_prof.username == "polyglotpete"
    assert pub_prof.followers_count >= 1
    assert pub_prof.is_following is True


def test_friends_leaderboard_scope(seeded_db: Session):
    user_demo = seeded_db.query(UserModel).filter_by(id="usr_demo").first()
    lb_service = LeaderboardService(seeded_db)

    res_global = lb_service.get_leaderboard(period="weekly", scope="global", current_user_id=user_demo.id)
    res_friends = lb_service.get_leaderboard(period="weekly", scope="friends", current_user_id=user_demo.id)

    assert res_global.total_participants >= res_friends.total_participants
    for entry in res_friends.entries:
        assert entry.user_id in (user_demo.id, "usr_polyglot", "usr_language_lover", "usr_spanish_pro")
