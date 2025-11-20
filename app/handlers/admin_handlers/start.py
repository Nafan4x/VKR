from aiogram import F, Router, types
from aiogram.filters import Filter, CommandStart
from aiogram.types import Message


from app.handlers.admin_handlers.filter import admin_filter
from app.db.session import get_db
from app.dao.user import UserDAO
from app.keyboards.admin_markup import Markup
from app.keyboards.callback_data import (
    start_page,
)


class AdminFilter(Filter):
    def __init__(self, admin_ids: list[int]):
        self.admin_ids = admin_ids

    async def __call__(self, event) -> bool:

        if isinstance(event, Message) or isinstance(event, types.CallbackQuery):
            return event.from_user.id in self.admin_ids
        return False


admin_router = Router()
admin_router.message.filter(admin_filter)


@admin_router.message(CommandStart())
async def start_command(message: Message):
    async for session in get_db():
        user, is_first = await UserDAO.update_or_create(
            session=session,
            telegram_id=message.from_user.id,
            username=message.from_user.username,
            full_name=message.from_user.full_name
        )

        await message.answer(
            '<b>Добро пожаловать в админ панель</b>',
            parse_mode='HTML',
            reply_markup=Markup.open_menu()
        )


@admin_router.callback_query(admin_filter, F.data == start_page)
async def start_menu(cb: types.CallbackQuery):
    await cb.message.edit_text(
        '<b>Добро пожаловать в админ панель</b>',
        parse_mode='HTML',
        reply_markup=Markup.open_menu()
    )
