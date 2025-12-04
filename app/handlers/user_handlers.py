from aiogram import F, Router, types
from aiogram.filters import CommandStart
from aiogram.types import InputMediaDocument, FSInputFile
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from app.config import config
from app.handlers.utils import exel_reader
from app.keyboards.markup import Markup
from app.keyboards.admin_markup import Markup as AdminMarkup
from app.keyboards.state import UserState
from app.dao.user import UserDAO
from app.dao.message import MessageDAO
from app.dao.resources import ResourcesDAO
from app.dao.feedback import FeedbackDAO
from app.dao.event import EventsDAO
from app.dao.social import SocialDAO
from app.dao.raffles import RaffleDAO, RaffleParticipantDAO
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
    input_feedback,
    member_card_page,
    ShowSocialCallback,
    RaffleAcceptCallback
)

router = Router()
start_message_text = '<b>Привет!</b>'


@router.message(CommandStart())
async def start_command(message: Message, state: FSMContext):
    await state.set_state(None)
    async for session in get_db():
        user, is_first = await UserDAO.update_or_create(
            session=session,
            telegram_id=message.from_user.id,
            username=message.from_user.username,
            full_name=message.from_user.full_name
        )
    text = message.text or ''

    parts = text.split(maxsplit=1)
    payload = parts[1] if len(parts) > 1 else None
    if payload and payload.startswith('raffle_'):
        raffle_id = int(payload.split('_')[1])
        async for session in get_db():
            raffle = await RaffleDAO.get_raffle_by_id(session=session, id=raffle_id)
        if raffle:
            await message.answer(
                f'Привет! Розыгрыш: {raffle.title}\n\n Нажми кнопку, чтобы участвовать.',
                reply_markup=Markup.raffle_accept_button(raffle_id)
            )
    await message.answer(
        start_message_text,
        parse_mode='HTML',
        reply_markup=Markup.open_menu()
    )


@router.callback_query(F.data == start_page)
async def start_menu(cb: types.CallbackQuery, state: FSMContext):
    await state.set_state(None)
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
        events = await EventsDAO.get_sorted_events(session=session)
    events_text = ''
    if events:
        for event in events:
            event_text = f'\n<b>{event[2]} - {event[0]}</b>\n<i>{event[1]}</i>\n'
            events_text += event_text
    message_text += '\n' + events_text
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
        socials = await SocialDAO.get_socials(session=session)
    await cb.message.edit_text(
        message_text,
        reply_markup=Markup.social_items_menu(socials),
        parse_mode='HTML',
    )


@router.callback_query(ShowSocialCallback.filter())
async def deleting_file(cb: types.CallbackQuery, callback_data: ShowSocialCallback):
    id = callback_data.id
    async for session in get_db():
        social = await SocialDAO.get_by_id(session=session, social_id=id)
    if social:
        await cb.message.edit_text(
            f'<b>🎉 {social[1]}</b>\n\n{social[2]}',
            parse_mode='HTML',
            reply_markup=Markup.back_special_menu(social_page)
        )
    else:
        await cb.message.edit_text(
            '❌ Ошибка',
            show_alert=True,
            reply_markup=Markup.back_special_menu(social_page)
        )


@router.callback_query(F.data == feedback_page)
async def feedback_menu(cb: types.CallbackQuery, state: FSMContext):
    await state.set_state(None)
    async for session in get_db():
        message_text = await MessageDAO.get_text_message(session, feedback_page)
    await cb.message.edit_text(
        message_text,
        reply_markup=Markup.feedback_menu(),
        parse_mode='HTML',
    )


@router.callback_query(F.data == input_feedback)
async def feedback_menu_2(cb: types.CallbackQuery, state: FSMContext):
    await state.set_state(UserState.input_feedback)
    message_text = 'Напишите сообщение в поддержку:'
    await cb.message.edit_text(
        message_text,
        reply_markup=Markup.back_special_menu(feedback_page),
        parse_mode='HTML',
    )


@router.message(F.text, UserState.input_feedback)
async def update_page_text(message: types.Message, state: FSMContext):
    await state.set_state(None)

    text_message = message.text

    async for session in get_db():
        feedback_id = await FeedbackDAO.create(
            session=session,
            from_user_id=message.chat.id,
            question=text_message
        )
    try:
        if config.ADMIN_IDS:
            for admin_id in config.ADMIN_IDS:
                await message.bot.send_message(
                    admin_id,
                    f"📩 Новое обращение в поддержку:\n\n"
                    f"👤 <b>Пользователь:</b> {message.chat.id}\n"
                    f"💬 <b>Вопрос:</b> {text_message}",
                    parse_mode="HTML",
                    reply_markup=AdminMarkup.feedback_reply(message.chat.id, feedback_id)
                )
            success_sending = True
        else: 
            success_sending = False
    except:
        success_sending = False
    if feedback_id and success_sending:
        await message.answer(
            '<b>✅ Ваш вопрос успешно отправлен!</b>',
            parse_mode='HTML',
        )
        await message.answer(
            text=start_message_text,
            parse_mode='HTML',
            reply_markup=Markup.open_menu()
        )
    else:
        await message.answer('❌ Ошибка при отправке вопроса', show_alert=True)


@router.callback_query(F.data == member_card_page)
async def member_menu(cb: types.CallbackQuery, state: FSMContext):
    await state.set_state(UserState.input_name)
    async for session in get_db():
        message_text = await MessageDAO.get_text_message(session, member_card_page)
    input_name_msg = await cb.message.edit_text(
        message_text,
        reply_markup=Markup.back_special_menu(start_page),
        parse_mode='HTML',
    )
    await state.set_data({'input_name_msg': input_name_msg})


@router.message(F.text, UserState.input_name)
async def input_name_msg(message: types.Message, state: FSMContext):
    data = await state.get_data()
    input_name_msg = data.get('input_name_msg')
    if input_name_msg:
        await input_name_msg.delete()
    await state.set_state(None)

    text_message = message.text
    print(text_message)
    member_card = await exel_reader.get_number_by_name(text_message)
    if member_card:
        await message.answer(
            f'<b>✅ Отлично!</b>\nФИО: <code>{text_message}</code>\nНомер билета: <code>{member_card}</code>',
            parse_mode='HTML',
        )
    else:
        await message.answer(
            f'<b>❌ Ошибка:</b> <i>ФИО "{text_message}" не найдено в базе данных</i>',
            parse_mode='HTML',
        )
    await message.answer(
        text=start_message_text,
        parse_mode='HTML',
        reply_markup=Markup.open_menu()
    )


@router.callback_query(RaffleAcceptCallback.filter())
async def join_raffle_handler(cb: types.CallbackQuery, callback_data: RaffleAcceptCallback, state: FSMContext):
    user_id = cb.from_user.id
    raffle_id = callback_data.id

    added = False
    async for session in get_db():
        added = await RaffleParticipantDAO.add_participant(session, raffle_id, user_id)
    if added:
        text = 'Вы успешно участвуете в розыгрыше!'
    else:
        text = 'Вы уже участвуете в этом розыгрыше.'

    await cb.answer(text=text, show_alert=False)
