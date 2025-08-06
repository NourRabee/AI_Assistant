from datetime import datetime, timezone, timedelta
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from db_config import Base


def two_minutes_from_now():
    return datetime.now(timezone.utc) + timedelta(minutes=10)


class PasswordResetToken(Base):
    __tablename__ = 'password_reset_token'

    id = Column(Integer, primary_key=True)
    token = Column(String(255), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="reset_tokens")
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    expires_at = Column(DateTime, default=two_minutes_from_now(), nullable=False)
    is_used = Column(Boolean, default=False)

