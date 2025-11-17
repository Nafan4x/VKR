from loguru import logger
from app.config import config

logger.add("bot.log", rotation="1 MB", level=config.LOG_LEVEL)
