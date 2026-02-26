from aiogram import Bot, Dispatcher

from app.config import config
# from app.logging import logger
from app.handlers import router


import typing
from aiogram import BaseMiddleware, types
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.exceptions import TelegramNetworkError
from aiohttp_socks import ProxyConnector
from app.dao.user import UserDAO
from app.db.session import get_db

from loguru import logger


def get_user_info(user: types.User) -> str:
    return f"{user.id} | {user.full_name} | @{user.username if user.username else 'Отсутствует'}"


logger.add("bot.log", rotation="10 MB", retention="30 days", level="INFO")


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


class BanMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        user_id = None
        if isinstance(event, types.Message):
            user_id = event.from_user.id
        elif isinstance(event, types.CallbackQuery):
            user_id = event.from_user.id

        async for session in get_db():
            is_banned = await UserDAO.is_banned(session=session, tg_id=user_id)
        if is_banned:
            # Забаненный пользователь - игнорируем
            if isinstance(event, types.Message):
                await event.answer("⛔ Вы забанены")
            elif isinstance(event, types.CallbackQuery):
                await event.answer("⛔ Вы забанены")
            return  # Не передаем дальше

        return await handler(event, data)


async def main():
    PROXY_URL = config.PROXY
   #  connector = ProxyConnector.from_url(PROXY_URL)
    session = AiohttpSession(proxy=PROXY_URL)
    bot = Bot(token=config.BOT_TOKEN, session=session)
    dp = Dispatcher()
    dp.message.outer_middleware(BanMiddleware())  # Сначала проверка бана
    dp.callback_query.outer_middleware(BanMiddleware())
    dp.message.outer_middleware(LogActionMiddleware())  # Потом логирование
    dp.callback_query.outer_middleware(LogActionMiddleware())
    # setup_middlewares(dispatcher)

    dp.include_router(router)

    logger.info('Bot starting...')
    await dp.start_polling(bot)
