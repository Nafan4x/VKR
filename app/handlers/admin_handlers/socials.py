from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext

import os

from app.handlers.admin_handlers.filter import admin_filter
from app.config import config
from app.keyboards.state import AdminState
from app.db.session import get_db
from app.dao.social import SocialDAO
from app.keyboards.admin_markup import Markup
from app.keyboards.callback_data import (
    edit_social,
    delete_social,
    add_social,
    DeleteSocialCallback
)


admin_router = Router()
admin_router.message.filter(admin_filter)


@admin_router.callback_query(admin_filter, F.data == edit_social)
async def edit_files_page(cb: types.CallbackQuery, state: FSMContext):
    await state.set_state(None)
    async for session in get_db():
        files = await SocialDAO.get_socials(session=session)
    message_text = 'Текущие соц. программы:\n\n'
    if files:
        for i in files:
            message_text += f'{i[0]}: {i[1]}\n'
    else:
        message_text += 'Пусто\n'
    message_text += '\n Для добавления или удаление файлов используйте кнопки ниже'
    await cb.message.edit_text(
        message_text,
        reply_markup=Markup.edit_social_menu(),
        parse_mode='HTML',
    )


@admin_router.callback_query(admin_filter, F.data == delete_social)
async def delete_files_page(cb: types.CallbackQuery):
    async for session in get_db():
        files = await SocialDAO.get_socials(session=session)
    message_text = 'Текущие соц. программы:\n\n'
    if files:
        for i in files:
            message_text += f'{i[0]}: {i[1]}\n'
        message_text += '\nВыберите id файла, который необходимо удалить с помощью кнопок⬇️'
        await cb.message.edit_text(
            message_text,
            reply_markup=Markup.delete_social_menu([file[0] for file in files]),
            parse_mode='HTML',
        )
    else:
        message_text += 'Пока нечего удалять'
        await cb.message.edit_text(
            message_text,
            reply_markup=Markup.back_special_menu(edit_social),
            parse_mode='HTML',
        )


@admin_router.callback_query(admin_filter, DeleteSocialCallback.filter())
async def deleting_file(cb: types.CallbackQuery, callback_data: DeleteSocialCallback):
    id = callback_data.id
    success = False
    async for session in get_db():
        success = await SocialDAO.delete_by_id(session=session, social_id=id)
    if success:
        await cb.message.edit_text(
            '<b>✅ Соц. программа успешно удалена!</b>',
            parse_mode='HTML',
            reply_markup=Markup.back_special_menu(edit_social)
        )
    else:
        await cb.message.edit_text(
            '❌ Ошибка при удалении соц. программы',
            show_alert=True,
            reply_markup=Markup.back_special_menu(edit_social)
        )


@admin_router.callback_query(admin_filter, F.data == add_social)
async def add_event_name_page(cb: types.CallbackQuery, state: FSMContext):
    await state.set_state(AdminState.add_social_name)
    message_text = 'Отправьте название соц. программы'
    await cb.message.edit_text(
        message_text,
        reply_markup=Markup.back_special_menu(edit_social),
        parse_mode='HTML',
    )


@admin_router.message(admin_filter, AdminState.add_social_name)
async def succefull_event_date_page(message: types.Message, state: FSMContext):
    social_name = message.text
    await state.set_state(AdminState.add_social_text)

    await state.update_data({'social_name': social_name})

    name_succes_msg = await message.answer(
        f'✅ Отлично, теперь отправьте текст для {social_name}:',
        parse_mode='HTML',
        reply_markup=Markup.back_special_menu(edit_social),
    )
    await state.update_data({'name_succes_msg': name_succes_msg})


@admin_router.message(admin_filter, AdminState.add_social_text)
async def succefull_event_text_page(message: types.Message, state: FSMContext):
    await state.set_state(None)

    event_text = message.text

    state_data = await state.get_data()
    event_name = state_data.get('social_name', 'Ошибка')

    async for session in get_db():
        event = await SocialDAO.update_or_create(
            session=session,
            name=event_name,
            description=event_text
        )

    name_succes_msg = state_data.get('name_succes_msg')

    await name_succes_msg.delete()

    if event:
        await message.answer(
            f'✅ Отлично, мероприятие {event_name} добавлено:',
            parse_mode='HTML',
            reply_markup=Markup.back_special_menu(edit_social),
        )
