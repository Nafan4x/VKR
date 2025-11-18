from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.keyboards.callback_data import (
    main_page,
    join_page,
    contact_page,
    feedback_page,
    event_page,
    social_page,
    start_page,
)


class Markup:
    @staticmethod
    def open_menu() -> InlineKeyboardMarkup:
        markup = InlineKeyboardBuilder()
        buttons_panel = [
            {
                'Главная 🏠': main_page
            },
            {
                'Как вступить? ✍️': join_page,
            },
            {
                'Социальные программы 🤝': social_page,
                'Мероприятия 🎉': event_page
            },
            {
                'Как связаться? 📞': contact_page,
                'Обратная связь 💬': feedback_page
            }
        ]
        for buttons in buttons_panel:
            markup.row(
                *[InlineKeyboardButton(text=key, callback_data=value) for key, value in buttons.items()]
            )

        return markup.as_markup()

    @staticmethod
    def back_menu() -> InlineKeyboardMarkup:
        markup = InlineKeyboardBuilder()
        markup.row(InlineKeyboardButton(text='⬅️ Вернуться назад', callback_data=start_page))
        return markup.as_markup()

    @staticmethod
    def feedback_menu(feedback_link) -> InlineKeyboardMarkup:
        markup = InlineKeyboardBuilder()
        markup.row(InlineKeyboardButton(text='Ссылка на форму', url=feedback_link))
        markup.row(InlineKeyboardButton(text='⬅️ Вернуться назад', callback_data=start_page))
        return markup.as_markup()
