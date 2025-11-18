from aiogram import F, Router, types
from aiogram.filters import CommandStart
from aiogram.types import InputMediaDocument, FSInputFile
from aiogram.types import Message


from app.keyboards.markup import Markup
from app.dao.user import UserDAO
from app.dao.message import MessageDAO
from app.dao.resources import ResourcesDAO
from app.db.session import get_db
from app.keyboards.callback_data import (
    start_page,
    main_page,
    contact_page,
    event_page,
    feedback_page,
    join_page,
    social_page,
    get_file_page,
)

router = Router()
start_message_text = '<b>Привет!</b>'


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
        start_message_text,
        parse_mode='HTML',
        reply_markup=Markup.open_menu()
    )


@router.callback_query(F.data == start_page)
async def start_menu(cb: types.CallbackQuery):
    await cb.message.edit_text(
        start_message_text,
        parse_mode='HTML',
        reply_markup=Markup.open_menu()
    )


@router.callback_query(F.data == main_page)
async def main_menu(cb: types.CallbackQuery):
    async for session in get_db():
        message_text = await MessageDAO.get_text_message(session, main_page)
    await cb.message.edit_text(
        message_text,
        reply_markup=Markup.back_menu(),
        parse_mode='HTML',
    )


@router.callback_query(F.data == contact_page)
async def contact_menu(cb: types.CallbackQuery):
    async for session in get_db():
        message_text = await MessageDAO.get_text_message(session, contact_page)
    await cb.message.edit_text(
        message_text,
        reply_markup=Markup.back_menu(),
        parse_mode='HTML',
    )


@router.callback_query(F.data == event_page)
async def event_menu(cb: types.CallbackQuery):
    async for session in get_db():
        message_text = await MessageDAO.get_text_message(session, event_page)
    await cb.message.edit_text(
        message_text,
        reply_markup=Markup.back_menu(),
        parse_mode='HTML',
    )


@router.callback_query(F.data == feedback_page)
async def feedback_menu(cb: types.CallbackQuery):
    async for session in get_db():
        message_text = await MessageDAO.get_text_message(session, feedback_page)
        link = await ResourcesDAO.get_resources(session=session, type='link')
    await cb.message.edit_text(
        message_text,
        reply_markup=Markup.feedback_menu(link),
        parse_mode='HTML',
    )


@router.callback_query(F.data == join_page)
async def join_menu(cb: types.CallbackQuery):
    async for session in get_db():
        message_text = await MessageDAO.get_text_message(session, join_page)
    await cb.message.edit_text(
        message_text,
        reply_markup=Markup.join_menu(),
        parse_mode='HTML',
    )


@router.callback_query(F.data == get_file_page)
async def get_file_menu(cb: types.CallbackQuery):
    sending_message = await cb.message.edit_text(
        'Отправляю файлы, пожалуйста подождите...',
        parse_mode='HTML',
    )
    async for session in get_db():
        files = await ResourcesDAO.get_resources(session, 'file')
        file_urls = [file[2] for file in files]
    if file_urls:
        media = [InputMediaDocument(media=FSInputFile(file_url)) for file_url in file_urls]
        await cb.message.answer_media_group(media)
    await sending_message.delete()
    await cb.message.answer(
        start_message_text,
        parse_mode='HTML',
        reply_markup=Markup.open_menu()
    )


@router.callback_query(F.data == social_page)
async def social_menu(cb: types.CallbackQuery):
    async for session in get_db():
        message_text = await MessageDAO.get_text_message(session, social_page)
    await cb.message.edit_text(
        message_text,
        reply_markup=Markup.back_menu(),
        parse_mode='HTML',
    )
