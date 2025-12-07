from sqlalchemy import select, asc
from sqlalchemy.ext.asyncio import AsyncSession

from dateutil import parser

from datetime import datetime, timedelta

from app.db.models.event import Event


class EventsDAO:
    @staticmethod
    async def get_events(
        session: AsyncSession,
    ) -> list:

        result = await session.execute(
            select(Event)
        )
        events = result.scalars().all()
        await session.commit()
        if events:
            return [
                (
                    event.id,
                    event.name,
                    event.date.strftime('%H:%M %d.%m.%Y'),
                    event.description)
                for event in events
            ]
        return None

    @staticmethod
    async def get_sorted_events(session: AsyncSession) -> list:
        now = datetime.utcnow()
        cutoff_time = now - timedelta(hours=2)

        result = await session.execute(
            select(Event)
            .where(Event.date >= cutoff_time)
            .order_by(asc(Event.date))
        )
        events = result.scalars().all()
        await session.commit()

        if events:
            return [
                (event.name, event.description, event.date.strftime('%H:%M %d.%m.%Y'))
                for event in events
            ]
        return None

    @staticmethod
    async def update_or_create(
        session: AsyncSession,
        name: str = None,
        description: str = None,
        date: str = None
    ) -> bool:

        result = await session.execute(
            select(Event).where(Event.name == name)
        )
        event = result.scalar_one_or_none()

        date = EventsDAO.parse_datetime(date)

        if not event:
            event = Event(name=name, description=description, date=date)
            session.add(event)
        else:
            event.description = description
            event.date = date

        await session.commit()
        await session.refresh(event)

        return True

    @staticmethod
    async def delete_by_id(session: AsyncSession, event_id: int) -> bool:
        result = await session.execute(
            select(Event).where(Event.id == event_id)
        )
        event = result.scalar_one_or_none()

        if not event:
            return False

        await session.delete(event)
        await session.commit()
        return True

    @staticmethod
    def parse_datetime(date_str: str):
        """
        Парсит строку в datetime и проверяет корректность ввода.

        - Поддерживает разные форматы через dateutil.parser
        - Проверяет, что строка не пустая
        - Возвращает None при ошибке и выводит сообщение
        """
        if not date_str or not date_str.strip():
            print("Ошибка: пустая строка")
            return None

        try:
            # Парсим дату
            date = parser.parse(date_str, dayfirst=True)

            # Пример проверки: дата не в прошлом (можно убрать, если не нужно)
            if date < datetime.now():
                print("Ошибка: дата уже прошла")
                return None

            return date
        except (ValueError, OverflowError) as ex:
            print(f"Ошибка при парсинге даты '{date_str}': {ex}")
            return None