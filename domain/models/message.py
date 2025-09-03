from datetime import datetime, timezone

from sqlalchemy import String, Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from db_config import Base


class Message(Base):
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True)
    conv_id = Column(Integer, ForeignKey('conversations.id'))
    conversation = relationship("Conversation", back_populates="messages")
    sender = Column(String(255), nullable=False)
    content = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
