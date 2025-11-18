from sqlalchemy import Column, Integer, String

from app.db.base import Base


class Message(Base):
    __tablename__ = 'message'

    id = Column(Integer, primary_key=True)
    page_name = Column(String, nullable=True)
    callback_text = Column(String, nullable=True)
    text = Column(String, nullable=True)
