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
    edit_text_messages,
    edit_events,
    edit_social,
    edit_form_link,
    EditPageCallback,
)


class Markup:
    @staticmethod
    def open_menu() -> InlineKeyboardMarkup:
        markup = InlineKeyboardBuilder()
        buttons_panel = [
            {'Изменить текст сообщений': edit_text_messages},
            {'Редактировать мероприятия': edit_events},
            {'Редактировать соц. программы': edit_social},
            {'Добавить/Изменить ссылку на форму': edit_form_link},
        ]
        for buttons in buttons_panel:
            markup.row(
                *[InlineKeyboardButton(text=key, callback_data=value) for key, value in buttons.items()]
            )

        return markup.as_markup()

    @staticmethod
    def open_edit_menu() -> InlineKeyboardMarkup:
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
                *[
                    InlineKeyboardButton(
                        text=key,
                        callback_data=EditPageCallback(page=value).pack()
                    )
                    for key, value in buttons.items()
                ]
            )
        markup.row(InlineKeyboardButton(text='⬅️ Вернуться назад', callback_data=start_page))

        return markup.as_markup()

    @staticmethod
    def back_menu() -> InlineKeyboardMarkup:
        markup = InlineKeyboardBuilder()
        markup.row(InlineKeyboardButton(text='⬅️ Вернуться назад', callback_data=start_page))
        return markup.as_markup()

    @staticmethod
    def back_special_menu(back_page: str) -> InlineKeyboardMarkup:
        markup = InlineKeyboardBuilder()
        markup.row(InlineKeyboardButton(text='⬅️ Вернуться назад', callback_data=back_page))
        return markup.as_markup()
