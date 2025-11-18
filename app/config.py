import os
from dataclasses import dataclass
from typing import List

from dotenv import load_dotenv

load_dotenv()


@dataclass
class Config:
    BOT_TOKEN: str = os.getenv('BOT_TOKEN')
    DB_URL: str = os.getenv('DB_URL', 'sqlite+aiosqlite:///database.db')
    LOG_LEVEL: str = os.getenv('LOG_LEVEL', 'INFO')
    ADMIN_IDS: List[int] = None

    def __init__(self):
        admin_ids_str = os.getenv('ADMIN_IDS', '')
        if admin_ids_str:
            self.ADMIN_IDS = [int(id.strip()) for id in admin_ids_str.split(',') if id.strip()]
        else:
            self.ADMIN_IDS = []


config = Config()