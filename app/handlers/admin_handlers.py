from aiogram import F, Router, types
from aiogram.filters import Filter, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

import os

from app.config import config
from app.keyboards.state import AdminState
from app.db.session import get_db
from app.dao.user import UserDAO
from app.dao.message import MessageDAO
from app.dao.resources import ResourcesDAO
from app.keyboards.admin_markup import Markup
from app.keyboards.callback_data import (
    start_page,
    edit_text_messages,
    edit_form_link,
    edit_files,
    delete_file,
    add_file,
    EditPageCallback,
    DeleteFileCallback
)


class AdminFilter(Filter):
    def __init__(self, admin_ids: list[int]):
        self.admin_ids = admin_ids

    async def __call__(self, event) -> bool:

        if isinstance(event, Message) or isinstance(event, types.CallbackQuery):
            return event.from_user.id in self.admin_ids
        return False


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


@admin_router.callback_query(admin_filter, F.data == start_page)
async def start_menu(cb: types.CallbackQuery):
    await cb.message.edit_text(
        '<b>Добро пожаловать в админ панель</b>',
        parse_mode='HTML',
        reply_markup=Markup.open_menu()
    )


@admin_router.callback_query(admin_filter, F.data == edit_text_messages)
async def edit_main_menu(cb: types.CallbackQuery, state: FSMContext):
    await state.set_state(None)
    message_text = 'Выберите, какую страницу редактировать'
    await cb.message.edit_text(
        message_text,
        reply_markup=Markup.open_edit_menu(),
        parse_mode='HTML',
    )


@admin_router.callback_query(admin_filter, EditPageCallback.filter())
async def edit_message(cb: types.CallbackQuery, callback_data: EditPageCallback, state: FSMContext):
    await state.set_state(AdminState.update_text)
    await state.set_data({'page': callback_data.page})
    message_text = f'Выбрана страница: {callback_data.page}.\nНапишите текст для страницы ниже:'
    await cb.message.edit_text(
        message_text,
        reply_markup=Markup.back_special_menu(edit_text_messages),
        parse_mode='HTML',
    )


@admin_router.message(admin_filter, F.text, AdminState.update_text)
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

    save_path = os.path.join(config.RESOURCE_PATH, filename)
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
