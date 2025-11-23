from sqlalchemy import Column, Integer, BigInteger, String, Boolean

from app.db.base import Base


class Feedback(Base):
    __tablename__ = 'feedback'

    id = Column(Integer, primary_key=True)
    from_user_id = Column(BigInteger, nullable=False)
    question = Column(String, nullable=True)
    answer = Column(String, nullable=True)
    is_active = Column(Boolean, nullable=False, default=True)
