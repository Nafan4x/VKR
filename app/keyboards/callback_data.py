from aiogram.filters.callback_data import CallbackData


class TestCallback(CallbackData, prefix="test"):
    action: str
    id: int