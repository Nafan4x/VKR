import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass
class Config:
    BOT_TOKEN: str = os.getenv('BOT_TOKEN')
    DB_URL: str = os.getenv('DB_URL', 'sqlite+aiosqlite:///database.db')
    LOG_LEVEL: str = os.getenv('LOG_LEVEL', 'INFO')


config = Config()
