from datetime import datetime, timezone

from sqlalchemy import String, Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from domain.models.base_model import BaseModel


class Conversation(BaseModel):

    __tablename__ = 'conversations'

    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="conversations")
    title = Column(String(255), nullable=True)
    last_activity = Column(DateTime, default=datetime.now(timezone.utc))
    messages = relationship("Message", back_populates="conversation")
