from aiogram import Bot, Dispatcher

from app.config import config
# from app.logging import logger
from app.handlers import router


import typing
from aiogram import BaseMiddleware, types

from loguru import logger


def get_user_info(user: types.User) -> str:
    return f"{user.id} | {user.full_name} | @{user.username if user.username else 'Отсутствует'}"


class LogActionMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: typing.Callable[[types.TelegramObject, typing.Dict[str, typing.Any]], typing.Awaitable[typing.Any]],
        event: types.TelegramObject,
        data: typing.Dict[str, typing.Any],
    ) -> typing.Any:
        if isinstance(event, types.Message):
            logger.info(f"{get_user_info(event.from_user)} - сообщение: {event.text}")
        elif isinstance(event, types.CallbackQuery):
            logger.info(f"{get_user_info(event.from_user)} - action: {event.data}")

        return await handler(event, data)


async def main():
    bot = Bot(token=config.BOT_TOKEN)
    dp = Dispatcher()
    dp.message.outer_middleware(LogActionMiddleware())
    dp.callback_query.outer_middleware(LogActionMiddleware())
    # setup_middlewares(dispatcher)

    dp.include_router(router)

    logger.info('Bot starting...')
    await dp.start_polling(bot)
