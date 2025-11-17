from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.keyboards.callback_data import (
    main_page,
    join_page,
    contact_page,
    feedback_page,
    event_page,
    social_page,
)


class Markup:
    @staticmethod
    def open_menu() -> InlineKeyboardMarkup:
        markup = InlineKeyboardBuilder()
        buttons_panel = [
            {'Главная': main_page},
            {'Как вступить?': join_page},
            {
                'Социальные программы': social_page,
                'Мероприятия': event_page
            },
            {
                'Как связаться?': contact_page,
                'Обратная связь': feedback_page
            }
        ]
        for buttons in buttons_panel:
            markup.row(
                *[InlineKeyboardButton(text=key, callback_data=value) for key, value in buttons.items()]
            )

        return markup.as_markup()
    # @staticmethod
    # def open_menu() -> InlineKeyboardMarkup:
    #     markup = InlineKeyboardBuilder()
    #     buttons = {
    #         'Главная': main_page,
    #         'Как вступить?': join_page,
    #         'Социальные программы': social_page,
    #         'Мероприятия': event_page,
    #         'Как связаться?': contact_page,
    #         'Обратная связь': feedback_page
    #     }

    #     for key, value in buttons.items():
    #         markup.row(
    #             InlineKeyboardButton(text=key, callback_data=value)
    #         )

    #     return markup.as_markup()
