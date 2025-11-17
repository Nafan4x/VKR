from aiogram import BaseMiddleware
from typing import Callable, Dict, Any
from app.db.session import async_session_maker

class DbSessionMiddleware(BaseMiddleware):
    async def __call__(self, handler: Callable, event, data: Dict[str, Any]):
        async with async_session_maker() as session:
            data["session"] = session
            return await handler(event, data)
