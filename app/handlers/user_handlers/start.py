from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message


from app.keyboards.markup import Markup
from app.dao.user import UserDAO
from app.db.session import get_db

router = Router()


@router.message(CommandStart())
async def start_command(message: Message):
    async for session in get_db():
        user, is_first = await UserDAO.update_or_create(
            session=session,
            telegram_id=message.from_user.id,
            username=message.from_user.username,
            full_name=message.from_user.full_name
        )

        await message.answer(
            '<b>Привет!</b>',
            parse_mode='HTML',
            reply_markup=Markup.open_menu()
        )
