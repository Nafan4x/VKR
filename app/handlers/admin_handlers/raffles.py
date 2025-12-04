from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext


from app.handlers.admin_handlers.filter import admin_filter
from app.keyboards.state import AdminState
from app.db.session import get_db
from app.dao.event import EventsDAO
from app.dao.user import UserDAO
from app.dao.raffles import RaffleDAO, RaffleParticipantDAO
from app.keyboards.admin_markup import Markup
from app.keyboards.callback_data import (
    add_raffle,
    raffle_page,
    PickWinnerCallback
)

admin_router = Router()
admin_router.message.filter(admin_filter)


@admin_router.callback_query(admin_filter, F.data == raffle_page)
async def raffle_menu(cb: types.CallbackQuery, state: FSMContext):
    await state.set_state(None)
    async for session in get_db():
        raffles = await RaffleDAO.get_raffles(session=session)
    raffles_text = ''
    for raffle in raffles:
        raffles_text += f'<code>{raffle[0]}</code>| {raffle[1]} | {raffle[2]} | {raffle[3]}\n'
    message_text = 'Розыгрыши:\n' + raffles_text
    await cb.message.edit_text(
        message_text,
        reply_markup=Markup.raffle_menu(raffles),
        parse_mode='HTML',
    )


@admin_router.callback_query(admin_filter, PickWinnerCallback.filter())
async def raffle_winner_page(cb: types.CallbackQuery, callback_data: PickWinnerCallback):
    raffle_id = callback_data.id
    async for session in get_db():
        winner_id = await RaffleParticipantDAO.pick_winner(session=session, raffle_id=raffle_id)
        user_data = await UserDAO.get_user_by_id(session=session, tg_id=winner_id)
    winner_text = f'tg_id: <code>{user_data.tg_id}</code>\nusername: <code>{user_data.username}</code>\nfull_name: <code>{user_data.full_name}</code>'
    message_text = 'Победитеть:\n' + winner_text
    await cb.message.edit_text(
        message_text,
        reply_markup=Markup.back_special_menu(raffle_page),
        parse_mode='HTML',
    )


@admin_router.callback_query(admin_filter, F.data == add_raffle)
async def add_raffle_title_page(cb: types.CallbackQuery, state: FSMContext):
    await state.set_state(AdminState.add_raffle_title)
    message_text = 'Отправьте название розыгрыша'
    await cb.message.edit_text(
        message_text,
        reply_markup=Markup.back_special_menu(raffle_page),
        parse_mode='HTML',
    )


@admin_router.message(admin_filter, AdminState.add_raffle_title)
async def add_raffle_description_page(message: types.Message, state: FSMContext):
    await state.set_state(AdminState.add_raffle_description)

    raffle_title = message.text
    await state.set_data({'raffle_title': raffle_title})
    raffle_title_msg = await message.answer(
        f'✅ Отлично, теперь отправьте описание для {raffle_title}',
        parse_mode='HTML',
        reply_markup=Markup.back_special_menu(raffle_page),
    )
    await state.update_data({'raffle_title_msg': raffle_title_msg})


@admin_router.message(admin_filter, AdminState.add_raffle_description)
async def add_raffle_start_date_page(message: types.Message, state: FSMContext):
    await state.set_state(AdminState.add_raffles_start_date)

    raffle_description = message.text
    await state.update_data({'raffle_description': raffle_description})
    raffle_description_msg = await message.answer(
        '✅ Отлично, теперь отправьте дату и время начала розыгрыша в формате "ч.м.г время"',
        parse_mode='HTML',
        reply_markup=Markup.back_special_menu(raffle_page),
    )
    await state.update_data({'raffle_description_msg': raffle_description_msg})


@admin_router.message(admin_filter, AdminState.add_raffles_start_date)
async def add_raffle_end_date_page(message: types.Message, state: FSMContext):

    event_date = message.text
    datetime_date_start = EventsDAO.parse_datetime(event_date)
    if not datetime_date_start:
        state_data = await state.get_data()
        raffle_description_msg = state_data.get('raffle_description_msg')
        raffle_title_msg = state_data.get('raffle_title_msg')
        if raffle_description_msg and raffle_title_msg:
            await raffle_description_msg.delete()
            await raffle_title_msg.delete()
        await message.answer(
            '⚠️ Пожалуйста, укажите корректую дату',
            reply_markup=Markup.back_special_menu(raffle_page)
        )
        return
    await state.set_state(AdminState.add_raffles_end_date)

    await state.update_data({'start_date': event_date})
    state_data = await state.get_data()
    raffle_title = state_data['raffle_title']

    date_start_succes_msg = await message.answer(
        f'✅ Отлично, теперь отправьте дату и время начала розыгрыша {raffle_title} в формате "ч.м.г время"',
        parse_mode='HTML',
        reply_markup=Markup.back_special_menu(raffle_page),
    )
    await state.update_data({'date_start_succes_msg': date_start_succes_msg})


@admin_router.message(admin_filter, AdminState.add_raffles_end_date)
async def succefull_raffle_page(message: types.Message, state: FSMContext):
    await state.set_state(None)

    state_data = await state.get_data()
    raffle_title = state_data.get('raffle_title', 'Ошибка')
    raffle_description = state_data.get('raffle_description', 'Ошибка')
    raffle_start_date = EventsDAO.parse_datetime(state_data.get('start_date', 'Ошибка'))
    raffle_end_date = EventsDAO.parse_datetime(message.text)

    async for session in get_db():
        event = await RaffleDAO.create_or_update(
            session=session,
            title=raffle_title,
            description=raffle_description,
            start_time=raffle_start_date,
            end_time=raffle_end_date
        )

    name_succes_msg = state_data.get('raffle_description_msg')
    date_succes_msg = state_data.get('raffle_title_msg')
    date_start_succes_msg = state_data.get('date_start_succes_msg')
    if name_succes_msg and date_succes_msg and date_start_succes_msg:
        await name_succes_msg.delete()
        await date_succes_msg.delete()
        await date_start_succes_msg.delete()

    if event:
        date_succes_msg = await message.answer(
            f'✅ Отлично, розыгрыш {raffle_title} добавлено:',
            parse_mode='HTML',
            reply_markup=Markup.back_special_menu(raffle_page),
        )
