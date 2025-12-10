from aiogram import Bot, Dispatcher

from app.config import config
from app.logging import logger
from app.handlers import router


async def main():
    bot = Bot(token=config.BOT_TOKEN)
    dp = Dispatcher()



    dp.include_router(router)

    logger.info('Bot starting...')
    await dp.start_polling(bot)
