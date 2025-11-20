from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext

from app.handlers.admin_handlers.filter import admin_filter
from app.keyboards.state import AdminState
from app.db.session import get_db
from app.dao.resources import ResourcesDAO
from app.keyboards.admin_markup import Markup
from app.keyboards.callback_data import (
    edit_form_link,
)

admin_router = Router()
admin_router.message.filter(admin_filter)


@admin_router.callback_query(admin_filter, F.data == edit_form_link)
async def edit_from_link(cb: types.CallbackQuery, state: FSMContext):
    await state.set_state(AdminState.add_form_link)
    message_text = 'Введите ссылку на форму'
    await cb.message.edit_text(
        message_text,
        reply_markup=Markup.back_menu(),
        parse_mode='HTML',
    )


@admin_router.message(admin_filter, F.text, AdminState.add_form_link)
async def update_form_link(message: types.Message, state: FSMContext):
    state.set_state(None)
    link = message.text
    success = False
    async for session in get_db():
        success = await ResourcesDAO.update_or_create(session=session, type='link', name='link', url=link)
    if success:
        await message.answer(
            f'<b>✅ Ссылка на форму успешно обновлёна!</b>\n<code>{link}</code>',
            parse_mode='HTML',
        )
        await message.answer(
            text='<b>Добро пожаловать в админ панель</b>',
            parse_mode='HTML',
            reply_markup=Markup.open_menu()
        )
    else:
        await message.answer('❌ Ошибка при обновлении ссылки на форму', show_alert=True)
