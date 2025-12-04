from sqlalchemy import select, asc
from sqlalchemy.ext.asyncio import AsyncSession

from datetime import datetime

from app.db.models.raffles import Raffle, RaffleParticipant


class RaffleDAO:
    @staticmethod
    async def get_raffles(session: AsyncSession) -> list:
        """Получить все розыгрыши"""
        result = await session.execute(select(Raffle))
        raffles = result.scalars().all()
        await session.commit()
        if raffles:
            return [
                (
                    raffle.id,
                    raffle.title,
                    raffle.start_time.strftime('%H:%M %d.%m.%Y'),
                    raffle.end_time.strftime('%H:%M %d.%m.%Y'),
                    raffle.description
                )
                for raffle in raffles
            ]
        return None

    @staticmethod
    async def get_raffle_by_id(session: AsyncSession, id: int) -> list:
        """Получить все розыгрыши"""
        result = await session.execute(select(Raffle).where(Raffle.id == id))
        raffle = result.scalar_one_or_none()
        await session.commit()
        if raffle:
            return raffle
        return None

    @staticmethod
    async def get_active_raffles(session: AsyncSession) -> list:
        """Получить только актуальные розыгрыши (по дате)"""
        now = datetime.utcnow()
        result = await session.execute(
            select(Raffle).where(Raffle.start_time <= now, Raffle.end_time >= now).order_by(asc(Raffle.start_time))
        )
        raffles = result.scalars().all()
        await session.commit()
        if raffles:
            return [
                (
                    raffle.id,
                    raffle.title,
                    raffle.start_time.strftime('%H:%M %d.%m.%Y'),
                    raffle.end_time.strftime('%H:%M %d.%m.%Y'),
                    raffle.description
                )
                for raffle in raffles
            ]
        return None

    @staticmethod
    async def create_or_update(
        session: AsyncSession,
        raffle_id: int = None,
        title: str = None,
        description: str = None,
        start_time: datetime = None,
        end_time: datetime = None
    ) -> bool:
        """Создать или обновить розыгрыш"""
        raffle = None
        if raffle_id:
            result = await session.execute(select(Raffle).where(Raffle.id == raffle_id))
            raffle = result.scalar_one_or_none()
        
        if title:
            result = await session.execute(select(Raffle).where(Raffle.title == title))
            raffle = result.scalar_one_or_none()

        if not raffle:
            raffle = Raffle(title=title, description=description, start_time=start_time, end_time=end_time)
            session.add(raffle)
        else:
            raffle.title = title
            raffle.description = description
            raffle.start_time = start_time
            raffle.end_time = end_time

        await session.commit()
        await session.refresh(raffle)
        return True

    @staticmethod
    async def delete_by_id(session: AsyncSession, raffle_id: int) -> bool:
        result = await session.execute(select(Raffle).where(Raffle.id == raffle_id))
        raffle = result.scalar_one_or_none()
        if not raffle:
            return False

        await session.delete(raffle)
        await session.commit()
        return True


class RaffleParticipantDAO:
    @staticmethod
    async def get_participants(session: AsyncSession, raffle_id: int) -> list:
        """Получить список участников конкретного розыгрыша"""
        result = await session.execute(select(RaffleParticipant).where(RaffleParticipant.raffle_id == raffle_id))
        participants = result.scalars().all()
        await session.commit()
        if participants:
            return [
                (p.user_id, p.joined_at.strftime('%H:%M %d.%m.%Y'))
                for p in participants
            ]
        return None

    @staticmethod
    async def add_participant(session: AsyncSession, raffle_id: int, user_id: int) -> bool:
        """Добавить участника, если его ещё нет"""
        result = await session.execute(
            select(RaffleParticipant)
            .where(RaffleParticipant.raffle_id == raffle_id, RaffleParticipant.user_id == user_id)
        )
        participant = result.scalar_one_or_none()
        if participant:
            return False  # уже участвует

        participant = RaffleParticipant(raffle_id=raffle_id, user_id=user_id)
        session.add(participant)
        await session.commit()
        await session.refresh(participant)
        return True

    @staticmethod
    async def delete_participant(session: AsyncSession, raffle_id: int, user_id: int) -> bool:
        """Удалить участника"""
        result = await session.execute(
            select(RaffleParticipant)
            .where(RaffleParticipant.raffle_id == raffle_id, RaffleParticipant.user_id == user_id)
        )
        participant = result.scalar_one_or_none()
        if not participant:
            return False

        await session.delete(participant)
        await session.commit()
        return True

    @staticmethod
    async def pick_winner(session: AsyncSession, raffle_id: int):
        """Выбрать случайного победителя розыгрыша"""
        import random
        result = await session.execute(
            select(RaffleParticipant).where(RaffleParticipant.raffle_id == raffle_id)
        )
        participants = result.scalars().all()
        if not participants:
            return None
        return random.choice(participants).user_id
