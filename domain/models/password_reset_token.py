from datetime import datetime, timezone, timedelta
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from domain.models.base_model import BaseModel


def two_minutes_from_now():
    return datetime.now(timezone.utc) + timedelta(minutes=10)


class PasswordResetToken(BaseModel):
    __tablename__ = 'password_reset_tokens'

    token = Column(String(255), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="reset_tokens")
    expires_at = Column(DateTime, default=two_minutes_from_now(), nullable=False)
    is_used = Column(Boolean, default=False)

