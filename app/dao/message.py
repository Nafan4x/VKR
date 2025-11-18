from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.message import Message


class MessageDAO:
    @staticmethod
    async def get_text_message(
        session: AsyncSession,
        callback_data: str,
    ) -> str:

        result = await session.execute(
            select(Message).where(Message.callback_text == callback_data)
        )
        message = result.scalar_one_or_none()
        message_text = 'Разработка'
        if message.text:
            message_text = message.text
        await session.commit()

        return message_text

    @staticmethod
    async def update_text_message(
        session: AsyncSession,
        callback_data: str,
        text: str
    ) -> bool:
        try:
            result = await session.execute(
                select(Message).where(Message.callback_text == callback_data)
            )
            message = result.scalar_one_or_none()

            if not message:
                return False

            message.text = text
            await session.commit()

            return True
        except Exception as e:
            await session.rollback()
            print(f"Ошибка при обновлении сообщения: {e}")
            return False
