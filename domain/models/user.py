from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship

from db_config import Base
from domain.models.base_model import BaseModel


class User(BaseModel):
    __tablename__ = 'users'

    full_name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    hashed_password = Column(String(512), nullable=False)
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))
    reset_tokens = relationship("PasswordResetToken", back_populates="user")
    conversations = relationship("Conversation", back_populates="user")
