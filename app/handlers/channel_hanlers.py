from aiogram import Router, types
from .utils.broadcast import broadcast_message_to_users

from app.dao.user import UserDAO
from app.db.session import get_db

channel_router = Router()

@channel_router.channel_post()
async def channel_post_handler(message: types.Message):
    user_ids= []
    async for session in get_db():
        user_ids = await UserDAO.get_all_users_ids(session=session)
    
    text_message = f"🆕 Новый пост в канале"
    
    await broadcast_message_to_users(
        bot=message.bot,
        user_ids=user_ids,
        text=text_message
    )   