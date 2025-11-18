from aiogram.filters.callback_data import CallbackData

# Admin callbacks
edit_text_messages = 'edit_text_messages_page'
edit_events = 'edit_events'
edit_social = 'edit_social'
edit_form_link = 'edit_form_link'
edit_files = 'edit_files'
delete_file = 'delete_file'
add_file = 'add_file'


class EditPageCallback(CallbackData, prefix='edit'):
    page: str


class DeleteFileCallback(CallbackData, prefix='del'):
    id: int


# User callbacks
start_page = 'start_page'
main_page = 'main_page'
social_page = 'social_page'
join_page = 'join_page'
event_page = 'event_page'
contact_page = 'contact_page'
feedback_page = 'feedback_page'
get_file_page = 'get_file_page'
delete_from_chat = 'delete_from_chat'
