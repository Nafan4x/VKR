from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext

import os

from app.handlers.admin_handlers.filter import admin_filter
from app.config import config
from app.keyboards.state import AdminState
from app.db.session import get_db
from app.dao.resources import ResourcesDAO
from app.keyboards.admin_markup import Markup
from app.keyboards.callback_data import (
    edit_files,
    delete_file,
    add_file,
    DeleteFileCallback
)


admin_router = Router()
admin_router.message.filter(admin_filter)


@admin_router.callback_query(admin_filter, F.data == edit_files)
async def edit_files_page(cb: types.CallbackQuery, state: FSMContext):
    await state.set_state(None)
    async for session in get_db():
        files = await ResourcesDAO.get_resources(session=session, type='file')
    message_text = 'Текущие файлы:\n\n'
    if files:
        for i in files:
            message_text += f'{i[0]}: {i[1]}\n'
    else:
        message_text += 'Пусто\n'
    message_text += '\n Для добавления или удаление файлов используйте кнопки ниже'
    await cb.message.edit_text(
        message_text,
        reply_markup=Markup.edit_files_menu(),
        parse_mode='HTML',
    )


@admin_router.callback_query(admin_filter, F.data == delete_file)
async def delete_files_page(cb: types.CallbackQuery):
    async for session in get_db():
        files = await ResourcesDAO.get_resources(session=session, type='file')
    message_text = 'Текущие файлы:\n\n'
    if files:
        for i in files:
            message_text += f'{i[0]}: {i[1]}\n'
        message_text += '\nВыберите id файла, который необходимо удалить с помощью кнопок⬇️'
        await cb.message.edit_text(
            message_text,
            reply_markup=Markup.delete_file_menu([file[0] for file in files]),
            parse_mode='HTML',
        )
    else:
        message_text += 'Пока нечего удалять'
        await cb.message.edit_text(
            message_text,
            reply_markup=Markup.back_special_menu(edit_files),
            parse_mode='HTML',
        )


@admin_router.callback_query(admin_filter, DeleteFileCallback.filter())
async def deleting_file(cb: types.CallbackQuery, callback_data: DeleteFileCallback):
    id = callback_data.id
    success = False
    async for session in get_db():
        success = await ResourcesDAO.delete_by_id(session=session, resource_id=id)
    if success:
        await cb.message.edit_text(
            '<b>✅ Файл успешно удален!</b>',
            parse_mode='HTML',
            reply_markup=Markup.back_special_menu(edit_files)
        )
    else:
        await cb.message.edit_text(
            '❌ Ошибка при удалении файла',
            show_alert=True,
            reply_markup=Markup.back_special_menu(edit_files)
        )


@admin_router.callback_query(admin_filter, F.data == add_file)
async def add_file_name_page(cb: types.CallbackQuery, state: FSMContext):
    await state.set_state(AdminState.add_file)
    message_text = 'Отправьте файл'
    await cb.message.edit_text(
        message_text,
        reply_markup=Markup.back_special_menu(edit_files),
        parse_mode='HTML',
    )


@admin_router.message(admin_filter, AdminState.add_file, F.document)
async def succefull_add_file_page(message: types.Message, state: FSMContext):
    await state.set_state(None)

    filename = message.document.file_name
    file_id = message.document.file_id
    downloading_msg = await message.answer('⬇️ Файл скачивается, пожалуйста, подождите...')

    file = await message.bot.get_file(file_id)
    file_path = file.file_path

    if not os.path.exists(f'{config.RESOURCE_PATH}/files'):
        os.makedirs(f'{config.RESOURCE_PATH}/files', exist_ok=True)
    save_path = os.path.join(f'{config.RESOURCE_PATH}/files', filename)
    await message.bot.download_file(file_path, destination=save_path)

    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    success = False
    async for session in get_db():
        success = await ResourcesDAO.update_or_create(
            session=session,
            type='file',
            name=filename,
            url=save_path
        )

    if success:
        await downloading_msg.edit_text(
            '<b>✅ Отлично, файл добавлен!</b>',
            parse_mode='HTML',
            reply_markup=Markup.back_special_menu(edit_files)
        )
    else:
        await downloading_msg.edit_text(
            '❌ Ошибка при добавлении файла, возможно файл с таким именем уже существует',
            show_alert=True,
            reply_markup=Markup.back_special_menu(edit_files),
        )
