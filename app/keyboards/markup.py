from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from app.keyboards.callback_data import TestCallback


def get_start_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton(
            text="Тестовая кнопка", 
            callback_data=TestCallback(action="test", id=1).pack()
        )]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)