import asyncio
from aiogram import Bot
from aiogram.exceptions import TelegramForbiddenError, TelegramNotFound

async def broadcast_message_to_users(bot: Bot, user_ids: list[int], text: str):
    """Отправляет уведомление о посте всем юзерам."""

    for user_id in user_ids:
        try:
            await bot.send_message(
                chat_id=user_id,
                text=text
            )
            await asyncio.sleep(0.05)

        except (TelegramForbiddenError, TelegramNotFound):
            pass

        except Exception as e:
            print(f"Ошибка рассылки для {user_id}: {e}")
