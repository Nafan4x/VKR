from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from datetime import datetime

from app.db.models.user import User
from app.db.base import Base


class Raffle(Base):
    __tablename__ = 'raffle'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)  # Название розыгрыша
    description = Column(String, nullable=True)  # Описание
    start_time = Column(DateTime(timezone=False), nullable=False, default=datetime.utcnow)
    end_time = Column(DateTime(timezone=False), nullable=False, default=datetime.utcnow)


class RaffleParticipant(Base):
    __tablename__ = 'raffle_participant'

    id = Column(Integer, primary_key=True)
    raffle_id = Column(Integer, nullable=False)  # ID розыгрыша
    user_id = Column(Integer, nullable=False)    # ID пользователя из таблицы User
    joined_at = Column(DateTime(timezone=False), default=datetime.utcnow)
