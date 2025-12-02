from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext

import os

from app.config import config
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
    await state.set_state(AdminState.add_exel_file)
    async for session in get_db():
        exel_data = await ResourcesDAO.get_resources(
            session=session,
            type='exel',
        )
    current_filename = exel_data.get('filename')
    current_filename_create_date = exel_data.get('create_date')
    message_text = f'Текущий файл:\n{current_filename} | {current_filename_create_date}\nЕсли нужно заменить, пришлите новый файл:'
    await cb.message.edit_text(
        message_text,
        reply_markup=Markup.back_menu(),
        parse_mode='HTML',
    )


@admin_router.message(admin_filter, AdminState.add_exel_file, F.document)
async def update_form_link(message: types.Message, state: FSMContext):
    await state.set_state(None)
    filename = message.document.file_name
    file_id = message.document.file_id
    downloading_msg = await message.answer('⬇️ Файл скачивается, пожалуйста, подождите...')

    file = await message.bot.get_file(file_id)
    file_path = file.file_path

    if not os.path.exists(f'{config.RESOURCE_PATH}/exel'):
        os.makedirs(f'{config.RESOURCE_PATH}/exel', exist_ok=True)
    save_path = os.path.join(f'{config.RESOURCE_PATH}/exel', filename)
    await message.bot.download_file(file_path, destination=save_path)

    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    success = False
    async for session in get_db():
        success = await ResourcesDAO.update_or_create(
            session=session,
            type='exel',
            name=filename,
            url=save_path
        )

    if success:
        await downloading_msg.edit_text(
            '<b>✅ Отлично, файл добавлен!</b>',
            parse_mode='HTML',
            reply_markup=Markup.back_special_menu(edit_form_link)
        )
    else:
        await downloading_msg.edit_text(
            '❌ Ошибка при добавлении файла, возможно файл с таким именем уже существует',
            show_alert=True,
            reply_markup=Markup.back_special_menu(edit_form_link),
        )
