from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext


from app.handlers.admin_handlers.filter import admin_filter
from app.keyboards.state import AdminState
from app.db.session import get_db
from app.dao.feedback import FeedbackDAO
from app.keyboards.admin_markup import Markup
from app.keyboards.callback_data import (
    DeleteMessageCallback
)


admin_router = Router()
admin_router.message.filter(admin_filter)


@admin_router.callback_query(F.data.startswith("reply_"))
async def start_reply(callback: types.CallbackQuery, state: FSMContext):
    user_id = int(callback.data.split("_")[1])
    feedback_id = int(callback.data.split("_")[2])
    async for session in get_db():
        isActiveFeedback = await FeedbackDAO.check_status_by_id(session=session, feedback_id=feedback_id)
    if isActiveFeedback:
        await state.set_state(AdminState.input_feedback_answer)
        await state.update_data({
            'reply_to_user_id':user_id,
            'feedback_id': feedback_id
        })
        input_message = await callback.message.answer(
            "Введите ответ пользователю:",
            reply_markup=Markup.delete_this_message(0) 
        )

        keyboard = Markup.delete_this_message(input_message.message_id)
        await input_message.edit_reply_markup(reply_markup=keyboard)
        await state.update_data({
            'input_message':input_message,
        })
    else:
        await callback.message.edit_text(
                "На данный вопрос уже ответили."
            )

@admin_router.callback_query(DeleteMessageCallback.filter())
async def delete_message_callback(callback: types.CallbackQuery, callback_data: DeleteMessageCallback):
    await callback.message.bot.delete_message(
        chat_id=callback.message.chat.id,
        message_id=callback_data.id
    )


@admin_router.message(admin_filter, F.text, AdminState.input_feedback_answer)
async def answer_feedback(message: types.Message, state: FSMContext):
    await state.set_state(None)
    data = await state.get_data()
    user_id = data.get('reply_to_user_id')
    feedback_id = data.get('feedback_id')
    input_message = data.get('input_message')
    answer_text = message.text
    feeback_item = False
    async for session in get_db():
        feeback_item = await FeedbackDAO.answer_by_id(
            session=session,
            feedback_id=feedback_id,
            answer=answer_text
        )
    try:
        await message.bot.send_message(
            int(user_id),
            f"📨 Ответ от поддержки:\n\n<i>{feeback_item.question}</i>\n\n<b>{answer_text}</b>",
            parse_mode='HTML'
        )
        success_sending = True
    except Exception as ex:
        print(ex)
        success_sending = False
    if feeback_item and success_sending:
        await input_message.delete()
        await message.answer(
            '<b>✅ Сообщение пользователю успешно отправлено!</b>',
            parse_mode='HTML',
        )
        await message.answer(
            text='<b>Добро пожаловать в админ панель</b>',
            parse_mode='HTML',
            reply_markup=Markup.open_menu()
        )
    else:
        await message.answer('❌ Ошибка при ответе пользователю', show_alert=True)
