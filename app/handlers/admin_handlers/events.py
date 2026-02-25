from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext


from app.handlers.admin_handlers.filter import admin_filter
from app.keyboards.state import AdminState
from app.db.session import get_db
from app.dao.event import EventsDAO
from app.keyboards.admin_markup import Markup
from app.keyboards.callback_data import (
    edit_events,
    delete_event,
    add_event,
    DeleteEventCallback
)


admin_router = Router()
admin_router.message.filter(admin_filter)


@admin_router.callback_query(admin_filter, F.data == edit_events)
async def edit_events_page(cb: types.CallbackQuery, state: FSMContext):
    await state.set_state(None)
    async for session in get_db():
        events = await EventsDAO.get_events(session=session)
    message_text = 'Текущие мероприятия:\n\n'
    if events:
        for i in events:
            message_text += f'<b>{i[0]}</b>: {i[1]}: \n{str(i[2])}\n<i>{i[3]}</i>\n'
    else:
        message_text += 'Пусто\n'
    message_text += '\n Для добавления или удаление мероприятий используйте кнопки ниже'
    await cb.message.edit_text(
        message_text,
        reply_markup=Markup.edit_events_menu(),
        parse_mode='HTML',
    )


@admin_router.callback_query(admin_filter, F.data == delete_event)
async def delete_files_page(cb: types.CallbackQuery):
    async for session in get_db():
        events = await EventsDAO.get_events(session=session)
    message_text = 'Текущие мероприятия:\n\n'
    if events:
        for i in events:
            message_text += f'{i[0]}: {i[1]}: {str(i[2])}\n'
        message_text += '\nВыберите id мероприятия, который необходимо удалить с помощью кнопок⬇️'
        await cb.message.edit_text(
            message_text,
            reply_markup=Markup.delete_events_menu([file[0] for file in events]),
            parse_mode='HTML',
        )
    else:
        message_text += 'Пока нечего удалять'
        await cb.message.edit_text(
            message_text,
            reply_markup=Markup.back_special_menu(edit_events),
            parse_mode='HTML',
        )


@admin_router.callback_query(admin_filter, DeleteEventCallback.filter())
async def deleting_file(cb: types.CallbackQuery, callback_data: DeleteEventCallback):
    id = callback_data.id
    success = False
    async for session in get_db():
        success = await EventsDAO.delete_by_id(session=session, event_id=id)
    if success:
        await cb.message.edit_text(
            '<b>✅ Мероприятие успешно удалено!</b>',
            parse_mode='HTML',
            reply_markup=Markup.back_special_menu(edit_events)
        )
    else:
        await cb.message.edit_text(
            '❌ Ошибка при удалении мероприятия',
            show_alert=True,
            reply_markup=Markup.back_special_menu(edit_events)
        )


@admin_router.callback_query(admin_filter, F.data == add_event)
async def add_event_name_page(cb: types.CallbackQuery, state: FSMContext):
    await state.set_state(AdminState.add_event_name)
    message_text = 'Отправьте название мероприятия'
    await cb.message.edit_text(
        message_text,
        reply_markup=Markup.back_special_menu(edit_events),
        parse_mode='HTML',
    )


@admin_router.message(admin_filter, AdminState.add_event_name)
async def succefull_event_name_page(message: types.Message, state: FSMContext):
    await state.set_state(AdminState.add_event_date)

    event_name = message.text
    await state.set_data({'event_name': event_name})
    name_succes_msg = await message.answer(
        f'✅ Отлично, теперь отправьте дату и время для {event_name} в формате "ч.м.г время"',
        parse_mode='HTML',
        reply_markup=Markup.back_special_menu(edit_events),
    )
    await state.update_data({'name_succes_msg': name_succes_msg})


@admin_router.message(admin_filter, AdminState.add_event_date)
async def succefull_event_date_page(message: types.Message, state: FSMContext):

    event_date = message.text
    datetime_date = EventsDAO.parse_datetime(event_date)
    if not datetime_date:
        state_data = await state.get_data()
        name_succes_msg = state_data.get('name_succes_msg')
        if name_succes_msg:
            await name_succes_msg.delete()
        await message.answer(
            '⚠️ Пожалуйста, укажите корректую дату',
            reply_markup=Markup.back_special_menu(edit_events)
        )
        return
    await state.set_state(AdminState.add_event_text)

    await state.update_data({'event_date': event_date})
    state_data = await state.get_data()
    event_name = state_data['event_name']

    date_succes_msg = await message.answer(
        f'✅ Отлично, теперь отправьте текст для {event_name}: {str(datetime_date)}',
        parse_mode='HTML',
        reply_markup=Markup.back_special_menu(edit_events),
    )
    await state.update_data({'date_succes_msg': date_succes_msg})


@admin_router.message(admin_filter, AdminState.add_event_text)
async def succefull_event_text_page(message: types.Message, state: FSMContext):
    await state.set_state(None)

    event_text = message.text

    state_data = await state.get_data()
    event_name = state_data.get('event_name', 'Ошибка')
    event_date = state_data.get('event_date', 'Ошибка')
    async for session in get_db():
        event = await EventsDAO.update_or_create(
            session=session,
            name=event_name,
            date=event_date,
            description=event_text
        )

    name_succes_msg = state_data.get('name_succes_msg')
    date_succes_msg = state_data.get('date_succes_msg')
    if name_succes_msg and date_succes_msg:
        await name_succes_msg.delete()
        await date_succes_msg.delete()

    if event:
        date_succes_msg = await message.answer(
            f'✅ Отлично, мероприятие {event_name} добавлено:',
            parse_mode='HTML',
            reply_markup=Markup.back_special_menu(edit_events),
        )
