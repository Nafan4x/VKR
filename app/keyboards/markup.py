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
    get_file_page,
    input_feedback,
    member_card_page,
    ShowSocialCallback
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
                'Номер билета ✍️': member_card_page,
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
    def feedback_menu() -> InlineKeyboardMarkup:
        markup = InlineKeyboardBuilder()
        markup.row(InlineKeyboardButton(text='Написать сообщение', callback_data=input_feedback))
        markup.row(InlineKeyboardButton(text='⬅️ Вернуться назад', callback_data=start_page))
        return markup.as_markup()

    @staticmethod
    def join_menu() -> InlineKeyboardMarkup:
        markup = InlineKeyboardBuilder()
        markup.row(InlineKeyboardButton(text='Получить файлы', callback_data=get_file_page))
        markup.row(InlineKeyboardButton(text='⬅️ Вернуться назад', callback_data=start_page))
        return markup.as_markup()

    @staticmethod
    def social_items_menu(socials) -> InlineKeyboardMarkup:
        markup = InlineKeyboardBuilder()
        for social in socials:
            markup.row(InlineKeyboardButton(text=f'{social[1]}', callback_data=ShowSocialCallback(id=social[0]).pack()))
        markup.row(InlineKeyboardButton(text='⬅️ Вернуться назад', callback_data=start_page))
        return markup.as_markup()

    @staticmethod
    def back_special_menu(back_page: str) -> InlineKeyboardMarkup:
        markup = InlineKeyboardBuilder()
        markup.row(InlineKeyboardButton(text='⬅️ Вернуться назад', callback_data=back_page))
        return markup.as_markup()
