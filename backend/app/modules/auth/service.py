import uuid
from sqlalchemy.orm import Session
from app.modules.user.models import UserModel
from app.modules.gamification.models import UserStatsModel
from app.modules.notifications.models import NotificationPreferenceModel
from app.shared.security import hash_password, verify_password, create_access_token
from app.shared.errors import ValidationError, UnauthorizedError
from app.shared.rate_limit import rate_limiter
from app.modules.auth.schemas import RegisterRequest, LoginRequest, AuthResponse
from app.modules.user.schemas import UserResponse


class AuthService:
    """Authentication, registration, credential verification & session management service."""

    def __init__(self, db: Session):
        self.db = db

    def register(self, req: RegisterRequest) -> AuthResponse:
        # Check duplicate email or username
        existing_email = self.db.query(UserModel).filter(UserModel.email == req.email).first()
        if existing_email:
            raise ValidationError("Email address is already registered.", code="DUPLICATE_EMAIL")

        existing_username = self.db.query(UserModel).filter(UserModel.username == req.username).first()
        if existing_username:
            raise ValidationError("Username is already taken.", code="DUPLICATE_USERNAME")

        user_id = f"usr_{uuid.uuid4().hex[:12]}"
        display_name = req.display_name or req.username.capitalize()

        user = UserModel(
            id=user_id,
            username=req.username,
            email=req.email,
            display_name=display_name,
            password_hash=hash_password(req.password),
            role="user",
            avatar=f"https://api.dicebear.com/7.x/bottts/svg?seed={req.username}",
        )
        self.db.add(user)

        # Initialize default UserStats
        stats = UserStatsModel(
            id=f"stats_{user_id}",
            user_id=user_id,
            total_xp=0,
            current_streak=0,
            longest_streak=0,
            hearts=5,
            gems=500,
            daily_goal_xp=20,
            daily_xp=0,
        )
        self.db.add(stats)

        # Initialize Notification Preferences
        pref = NotificationPreferenceModel(
            id=f"pref_{user_id}",
            user_id=user_id,
            daily_reminders=True,
            streak_reminders=True,
            quest_reminders=True,
            social_notifications=True,
            achievement_notifications=True,
        )
        self.db.add(pref)

        self.db.commit()
        self.db.refresh(user)

        access_token = create_access_token(user.id, role=user.role)
        return AuthResponse(user=UserResponse.model_validate(user), access_token=access_token)

    def login(self, req: LoginRequest, client_ip: str = "127.0.0.1") -> AuthResponse:
        # Rate limit login abuse per IP
        rate_limiter.check(f"login_{client_ip}", limit=10, window_seconds=60)

        # Lookup user by email or username
        user = (
            self.db.query(UserModel)
            .filter(
                (UserModel.email == req.email_or_username) | (UserModel.username == req.email_or_username)
            )
            .first()
        )

        if not user or not user.password_hash or not verify_password(req.password, user.password_hash):
            rate_limiter.consume(f"login_{client_ip}", limit=10, window_seconds=60)
            raise UnauthorizedError("Invalid email or password.", code="INVALID_CREDENTIALS")

        if not user.is_active:
            raise UnauthorizedError("Account has been disabled.", code="ACCOUNT_DISABLED")

        access_token = create_access_token(user.id, role=user.role)
        return AuthResponse(user=UserResponse.model_validate(user), access_token=access_token)
