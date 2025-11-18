from aiogram import F, Router, types
from aiogram.filters import Filter, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from app.config import config
from app.keyboards.state import AdminState
from app.db.session import get_db
from app.dao.user import UserDAO
from app.dao.message import MessageDAO
from app.keyboards.admin_markup import Markup
from app.keyboards.callback_data import (
    start_page,
    edit_text_messages,
    EditPageCallback
)


class AdminFilter(Filter):
    def __init__(self, admin_ids: list[int]):
        self.admin_ids = admin_ids

    async def __call__(self, message: Message) -> bool:
        return message.from_user.id in self.admin_ids


admin_filter = AdminFilter(config.ADMIN_IDS)

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


@admin_router.callback_query(F.data == start_page)
async def start_menu(cb: types.CallbackQuery):
    await cb.message.edit_text(
        '<b>Добро пожаловать в админ панель</b>',
        parse_mode='HTML',
        reply_markup=Markup.open_menu()
    )


@admin_router.callback_query(F.data == edit_text_messages)
async def edit_main_menu(cb: types.CallbackQuery, state: FSMContext):
    await state.set_state(None)
    message_text = 'Выберите, какую страницу редактировать'
    await cb.message.edit_text(
        message_text,
        reply_markup=Markup.open_edit_menu(),
        parse_mode='HTML',
    )


@admin_router.callback_query(EditPageCallback.filter())
async def edit_message(cb: types.CallbackQuery, callback_data: EditPageCallback, state: FSMContext):
    await state.set_state(AdminState.update_text)
    await state.set_data({'page': callback_data.page})
    message_text = f'Выбрана страница: {callback_data.page}.\nНапишите текст для страницы ниже:'
    await cb.message.edit_text(
        message_text,
        reply_markup=Markup.back_special_menu(edit_text_messages),
        parse_mode='HTML',
    )


@admin_router.message(F.text, AdminState.update_text)
async def update_page_text(message: types.Message, state: FSMContext):
    await state.set_state(None)
    data = await state.get_data()
    page = data.get('page')
    text_message = message.text
    success = False
    async for session in get_db():
        success = await MessageDAO.update_text_message(session=session, callback_data=page, text=text_message)
    if success:
        await message.answer(
            '<b>✅ Текст сообщения успешно обновлён!</b>',
            parse_mode='HTML',
        )
        await message.answer(
            text='<b>Добро пожаловать в админ панель</b>',
            parse_mode='HTML',
            reply_markup=Markup.open_menu()
        )
    else:
        await message.answer('❌ Ошибка при обновлении текста страницы', show_alert=True)
