import os
from dataclasses import dataclass
from typing import List

from dotenv import load_dotenv

load_dotenv()


@dataclass
class Config:
    BOT_TOKEN: str = os.getenv('BOT_TOKEN')
    BOT_USERNAME: str = os.getenv('BOT_USERNAME')
    DB_URL: str = os.getenv('DB_URL', 'sqlite+aiosqlite:///database.db')
    LOG_LEVEL: str = os.getenv('LOG_LEVEL', 'INFO')
    PROXY: str = os.getenv('PROXY')
    ADMIN_IDS: List[int] = None
    RESOURCE_PATH: str = None

    def __init__(self):
        # ADMIN_IDS
        admin_ids_str = os.getenv('ADMIN_IDS', '')
        if admin_ids_str:
            self.ADMIN_IDS = [int(id.strip()) for id in admin_ids_str.split(',') if id.strip()]
        else:
            self.ADMIN_IDS = []

        resource_path_env = os.getenv('RESOURCE_PATH', 'resources')

        self.RESOURCE_PATH = os.path.abspath(resource_path_env)

        if not os.path.exists(self.RESOURCE_PATH):
            os.makedirs(self.RESOURCE_PATH, exist_ok=True)


config = Config()
