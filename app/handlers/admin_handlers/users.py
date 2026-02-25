from aiogram import F, Router, types
from aiogram.types import BufferedInputFile
from aiogram.fsm.context import FSMContext
from datetime import datetime


from app.handlers.admin_handlers.filter import admin_filter
from app.keyboards.state import AdminState
from app.db.session import get_db
from app.dao.user import UserDAO
from app.keyboards.admin_markup import Markup
from app.handlers.utils.create_users_file import create_table_txt
from app.keyboards.callback_data import (
    get_users_list,
    ban_user_panel,
    open_users
)

admin_router = Router()
admin_router.message.filter(admin_filter)
start_userse_message_text = '<b>Выберите действие:</b>'


@admin_router.callback_query(admin_filter, F.data == open_users)
async def open_users_menu(cb: types.CallbackQuery, state: FSMContext):
    await state.set_state(None)
    await cb.message.edit_text(
        start_userse_message_text,
        parse_mode='HTML',
        reply_markup=Markup.open_users_menu()
    )


@admin_router.callback_query(admin_filter, F.data == get_users_list)
async def open_get_user_list_menu(cb: types.CallbackQuery, state: FSMContext):
    await state.set_state(None)
    sending_message = await cb.message.edit_text(
        'Отправляю файл c пользователями, пожалуйста подождите...',
        parse_mode='HTML',
    )
    async for session in get_db():  
        users_list = await UserDAO.get_all_users_info(session)
        users_file = await create_table_txt(users_list)
    if users_file:
        filename = f"users_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        await cb.message.answer_document(
            document=BufferedInputFile(
                file=users_file.getvalue(),
                filename=filename
            )
        )
        users_file.close()
    await sending_message.delete()
    await cb.message.answer(
        start_userse_message_text,
        parse_mode='HTML',
        reply_markup=Markup.open_users_menu()
    )


@admin_router.callback_query(admin_filter, F.data == ban_user_panel)
async def open_ban_user_menu(cb: types.CallbackQuery, state: FSMContext):
    await state.set_state(AdminState.delete_user)
    await cb.message.edit_text(
        '<b>Введите tg_id пользователя, которого хотите забанить</b>',
        parse_mode='HTML',
        reply_markup=Markup.back_menu()
    )

 
@admin_router.message(admin_filter, AdminState.delete_user)
async def succes_ban_user_panel(message: types.Message, state: FSMContext):
    # await state.set_state(AdminState.add_raffle_description)

    ban_user_id = message.text
    succes_ban = False
    async for session in get_db():
        succes_ban = await UserDAO.ban_user(session=session, tg_id=ban_user_id)
    if succes_ban:
        await state.set_state(None)
        await message.answer(
            f'✅ Пользователь с tg_id: {ban_user_id} успешно заблокирован',
            parse_mode='HTML',
        )        
        await message.answer(
            start_userse_message_text,
            parse_mode='HTML',
            reply_markup=Markup.open_users_menu()
        )
    else:
        await message.answer(
            '<b>Не найден пользователь с таким tg_id, повторите попытку</b>',
            parse_mode='HTML',
            reply_markup=Markup.back_menu()
        )
