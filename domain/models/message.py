from sqlalchemy import String, Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from domain.models.base_model import BaseModel


class Message(BaseModel):
    __tablename__ = 'messages'

    conv_id = Column(Integer, ForeignKey('conversations.id'))
    conversation = relationship("Conversation", back_populates="messages")
    sender = Column(String(255), nullable=False)
    content = Column(String(255), nullable=False)
