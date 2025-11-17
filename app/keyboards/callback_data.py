from aiogram.filters.callback_data import CallbackData


start_page = "call_start_page"


class TestCallback(CallbackData, prefix="test"):
    action: str
    id: int
