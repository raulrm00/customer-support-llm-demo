from sqlalchemy.orm import Session

from app.core import security
from app.core.config import get_settings
from app.models.user import User

settings = get_settings()


def init_db(db: Session) -> None:
    """Initialize the database with some test users."""
    # Create admin user if it doesn't exist
    admin_email = "admin@example.com"
    admin = db.query(User).filter(User.email == admin_email).first()
    if not admin:
        admin = User(
            email=admin_email,
            password_hash=security.get_password_hash("password123"),
            is_admin=True,
            daily_limit_seconds=settings.default_daily_limit_seconds,
        )
        db.add(admin)

    # Create normal user if it doesn't exist
    user_email = "user@example.com"
    user = db.query(User).filter(User.email == user_email).first()
    if not user:
        user = User(
            email=user_email,
            password_hash=security.get_password_hash("password123"),
            is_admin=False,
            daily_limit_seconds=settings.default_daily_limit_seconds,
        )
        db.add(user)

    db.commit()
