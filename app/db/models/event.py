from sqlalchemy import Column, Integer, String, DateTime

from datetime import datetime

from app.db.base import Base


class Event(Base):
    __tablename__ = 'event'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=True)
    description = Column(String, nullable=True)

    date = Column(
        DateTime(timezone=False),
        default=datetime(2010, 1, 1, 12, 0),
        nullable=False
    )
