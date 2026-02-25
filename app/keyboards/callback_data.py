from aiogram.filters.callback_data import CallbackData

# Admin callbacks
# outer callbacks
open_edit_items = 'open_edit_items'
raffle_page = 'raffle_page'
open_users = 'open_users'


# inner callbacks
edit_text_messages = 'edit_text_messages_page'
edit_events = 'edit_events'
edit_social = 'edit_social'
edit_form_link = 'edit_form_link'
edit_files = 'edit_files'
delete_file = 'delete_file'
add_file = 'add_file'

edit_event = 'edit_event'
delete_event = 'delete_event'
add_event = 'add_event'
add_raffle = 'add_raffle'
delete_raffle = 'delete_raffle'

edit_social = 'edit_social'
delete_social = 'delete_social'
add_social = 'add_social'

get_users_list = 'get_users_list'
ban_user_panel = 'ban_user_panel'

pick_raffle_winner = 'pick_raffle_winner'


class EditPageCallback(CallbackData, prefix='edit'):
    page: str


class DeleteFileCallback(CallbackData, prefix='del'):
    id: int

class DeleteMessageCallback(CallbackData, prefix='del-msg'):
    id: int

class DeleteEventCallback(CallbackData, prefix='del-event'):
    id: int


class DeleteSocialCallback(CallbackData, prefix='del-social'):
    id: int

class DeleteRafflesCallback(CallbackData, prefix='del-raffles'):
    id: int

class PickWinnerCallback(CallbackData, prefix='raf_win'):
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
member_card_page = 'member_card_page'

input_feedback = 'input_feedback'
input_name = 'input_name'


class ShowSocialCallback(CallbackData, prefix='show-social'):
    id: int


class RaffleAcceptCallback(CallbackData, prefix='raf_apt'):
    id: int
