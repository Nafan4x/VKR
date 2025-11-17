from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message


from app.keyboards.markup import Markup

router = Router()


@router.message(CommandStart())
async def start_command(message: Message):
    await message.answer(
        '<b>Привет!</b>',
        parse_mode='HTML',
        reply_markup=Markup.open_menu()
    )
