from aiogram.fsm.state import StatesGroup, State


class AdminState(StatesGroup):
    update_text = State()

    add_event_text = State()
    add_exel_file = State()
    add_file = State()

    add_event_name = State()
    add_event_date = State()

    add_social_name = State()
    add_social_text = State()

    input_feedback_answer = State()


class UserState(StatesGroup):
    input_feedback = State()
    input_name = State()
