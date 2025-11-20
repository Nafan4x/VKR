from aiogram import types
from aiogram.filters import Filter
from aiogram.types import Message

from app.config import config


class AdminFilter(Filter):
    def __init__(self, admin_ids: list[int]):
        self.admin_ids = admin_ids

    async def __call__(self, event) -> bool:

        if isinstance(event, Message) or isinstance(event, types.CallbackQuery):
            return event.from_user.id in self.admin_ids
        return False


admin_filter = AdminFilter(config.ADMIN_IDS)
