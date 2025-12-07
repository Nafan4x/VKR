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
    edit_files,
    delete_file,
    add_event,
    delete_event,
    delete_raffle,
    add_file,
    delete_social,
    add_social,
    add_raffle,
    member_card_page,
    pick_raffle_winner,
    raffle_page,
    EditPageCallback,
    DeleteFileCallback,
    DeleteEventCallback,
    DeleteSocialCallback,
    DeleteMessageCallback,
    PickWinnerCallback,
    DeleteRafflesCallback
)


class Markup:
    @staticmethod
    def open_menu() -> InlineKeyboardMarkup:
        markup = InlineKeyboardBuilder()
        buttons_panel = [
            {'Изменить текст сообщений': edit_text_messages},
            {'Редактировать мероприятия': edit_events},
            {'Редактировать соц. программы': edit_social},
            {'Розыгрыши': raffle_page},
            {'Добавить/Изменить exel файл': edit_form_link},
            {'Добавить/Изменить файлы для поступления': edit_files},
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
            {'Как вступить?': join_page,
             'Номер билета': member_card_page},
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

    @staticmethod
    def edit_files_menu() -> InlineKeyboardMarkup:
        markup = InlineKeyboardBuilder()
        markup.row(
            InlineKeyboardButton(text='➖', callback_data=delete_file),
            InlineKeyboardButton(text='➕', callback_data=add_file),
        )
        markup.row(InlineKeyboardButton(text='⬅️ Вернуться назад', callback_data=start_page))
        return markup.as_markup()

    @staticmethod
    def delete_file_menu(files_ids: list) -> InlineKeyboardMarkup:
        markup = InlineKeyboardBuilder()
        row_buttons = []

        for i, file_id in enumerate(files_ids, start=1):
            button = InlineKeyboardButton(
                text=f'{file_id}',
                callback_data=DeleteFileCallback(id=file_id).pack()
            )
            row_buttons.append(button)
            if i % 5 == 0:
                markup.row(*row_buttons)
                row_buttons = []
        if row_buttons:
            markup.row(*row_buttons)
        markup.row(
            InlineKeyboardButton(text='⬅️ Вернуться назад', callback_data=start_page)
        )
        return markup.as_markup()

    @staticmethod
    def edit_events_menu() -> InlineKeyboardMarkup:
        markup = InlineKeyboardBuilder()
        markup.row(
            InlineKeyboardButton(text='➖', callback_data=delete_event),
            InlineKeyboardButton(text='➕', callback_data=add_event),
        )
        markup.row(InlineKeyboardButton(text='⬅️ Вернуться назад', callback_data=start_page))
        return markup.as_markup()

    @staticmethod
    def delete_events_menu(files_ids: list) -> InlineKeyboardMarkup:
        markup = InlineKeyboardBuilder()
        row_buttons = []

        for i, file_id in enumerate(files_ids, start=1):
            button = InlineKeyboardButton(
                text=f'{file_id}',
                callback_data=DeleteEventCallback(id=file_id).pack()
            )
            row_buttons.append(button)
            if i % 5 == 0:
                markup.row(*row_buttons)
                row_buttons = []
        if row_buttons:
            markup.row(*row_buttons)
        markup.row(
            InlineKeyboardButton(text='⬅️ Вернуться назад', callback_data=start_page)
        )
        return markup.as_markup()

    @staticmethod
    def edit_social_menu() -> InlineKeyboardMarkup:
        markup = InlineKeyboardBuilder()
        markup.row(
            InlineKeyboardButton(text='➖', callback_data=delete_social),
            InlineKeyboardButton(text='➕', callback_data=add_social),
        )
        markup.row(InlineKeyboardButton(text='⬅️ Вернуться назад', callback_data=start_page))
        return markup.as_markup()

    @staticmethod
    def raffle_menu(raffles) -> InlineKeyboardMarkup:
        markup = InlineKeyboardBuilder()
        markup.row(
            InlineKeyboardButton(text='➖', callback_data=delete_raffle),
            InlineKeyboardButton(text='➕', callback_data=add_raffle),
        )
        if raffles:
            for raffle in raffles:
                markup.row(
                    InlineKeyboardButton(
                        text=f'Выбрать победителя для розыгрыша {raffle[0]}',
                        callback_data=PickWinnerCallback(id=raffle[0]).pack()),
                )
        markup.row(InlineKeyboardButton(text='⬅️ Вернуться назад', callback_data=start_page))
        return markup.as_markup()

    @staticmethod
    def delete_social_menu(files_ids: list) -> InlineKeyboardMarkup:
        markup = InlineKeyboardBuilder()
        row_buttons = []

        for i, file_id in enumerate(files_ids, start=1):
            button = InlineKeyboardButton(
                text=f'{file_id}',
                callback_data=DeleteSocialCallback(id=file_id).pack()
            )
            row_buttons.append(button)
            if i % 5 == 0:
                markup.row(*row_buttons)
                row_buttons = []
        if row_buttons:
            markup.row(*row_buttons)
        markup.row(
            InlineKeyboardButton(text='⬅️ Вернуться назад', callback_data=start_page)
        )
        return markup.as_markup()

    @staticmethod
    def feedback_reply(chat_id, feedback_id) -> InlineKeyboardMarkup:
        markup = InlineKeyboardBuilder()
        markup.row(
                InlineKeyboardButton(
                text="✉️ Ответить",
                callback_data=f"reply_{chat_id}_{feedback_id}"
            )
        )
        return markup.as_markup()

    @staticmethod
    def delete_this_message(msg_id) -> InlineKeyboardMarkup:
        markup = InlineKeyboardBuilder()
        markup.row(
                InlineKeyboardButton(
                text="Не отвечать",
                callback_data=DeleteMessageCallback(id=msg_id).pack()
            )
        )
        return markup.as_markup()
    
    @staticmethod
    def delete_raffles_menu(raffles_ids: list) -> InlineKeyboardMarkup:
        markup = InlineKeyboardBuilder()
        row_buttons = []
        if raffles_ids:
            for i, file_id in enumerate(raffles_ids, start=1):
                button = InlineKeyboardButton(
                    text=f'{file_id}',
                    callback_data=DeleteRafflesCallback(id=file_id).pack()
                )
                row_buttons.append(button)
                if i % 5 == 0:
                    markup.row(*row_buttons)
                    row_buttons = []
            if row_buttons:
                markup.row(*row_buttons)
        markup.row(
            InlineKeyboardButton(text='⬅️ Вернуться назад', callback_data=raffle_page)
        )
        return markup.as_markup()