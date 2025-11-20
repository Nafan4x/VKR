from sqlalchemy import Column, Integer, String

from app.db.base import Base


class Social(Base):
    __tablename__ = 'social'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=True)
    description = Column(String, nullable=True)
