from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime

from app.db.base import Base


class Resources(Base):
    __tablename__ = 'resources'

    id = Column(Integer, primary_key=True)
    type = Column(String, nullable=True)
    name = Column(String, nullable=True)
    url = Column(String, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)