from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery, Message


from app.keyboards.callback_data import TestCallback
from app.keyboards.markup import get_start_keyboard

router = Router()


@router.message(CommandStart())
async def start_command(message: Message):
    keyboard = get_start_keyboard()
    await message.answer(
        'Привет! Это тестовый бот. Нажми кнопку ниже:',
        reply_markup=keyboard
    )


@router.callback_query(TestCallback.filter(F.action == 'test'))
async def handle_test_callback(callback: CallbackQuery, callback_data: TestCallback):
    await callback.answer()
    await callback.message.answer(f'Вы нажали кнопку! ID: {callback_data.id}')
