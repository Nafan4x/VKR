from aiogram.filters.callback_data import CallbackData

# Admin callbacks
edit_text_messages = 'edit_text_messages_page'
edit_events = 'edit_events'
edit_social = 'edit_social'


class EditPageCallback(CallbackData, prefix='edit'):
    page: str


# User callbacks
start_page = 'start_page'
main_page = 'main_page'
social_page = 'social_page'
join_page = 'join_page'
event_page = 'event_page'
contact_page = 'contact_page'
feedback_page = 'feedback_page'
