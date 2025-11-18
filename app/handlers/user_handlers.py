from aiogram import F, Router, types
from aiogram.filters import CommandStart
from aiogram.types import Message


from app.keyboards.markup import Markup
from app.dao.user import UserDAO
from app.dao.message import MessageDAO
from app.db.session import get_db
from app.keyboards.callback_data import (
    start_page,
    main_page,
    contact_page,
    event_page,
    feedback_page,
    join_page,
    social_page,
)

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


@router.callback_query(F.data == start_page)
async def start_menu(cb: types.CallbackQuery):
    await cb.message.edit_text(
        '<b>Привет!</b>',
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
        await cb.message.edit_text(
            message_text,
            reply_markup=Markup.back_menu(),
            parse_mode='HTML',
        )


@router.callback_query(F.data == join_page)
async def join_menu(cb: types.CallbackQuery):
    async for session in get_db():
        message_text = await MessageDAO.get_text_message(session, join_page)
        await cb.message.edit_text(
            message_text,
            reply_markup=Markup.back_menu(),
            parse_mode='HTML',
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
