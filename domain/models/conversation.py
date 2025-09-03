from datetime import datetime, timezone

from sqlalchemy import String, Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from db_config import Base


class Conversation(Base):

    __tablename__ = 'conversations'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="conversations")
    title = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    last_activity = Column(DateTime, default=datetime.now(timezone.utc))
    messages = relationship("Message", back_populates="conversation")
