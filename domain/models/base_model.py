from sqlalchemy import Column, Integer, DateTime
from datetime import datetime, timezone

from db_config import Base


class BaseModel(Base):
    __abstract__ = True  # prevents table creation

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
