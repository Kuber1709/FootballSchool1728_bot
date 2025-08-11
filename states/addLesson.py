from aiogram.fsm.state import StatesGroup, State


class AddLesson(StatesGroup):
    menu_id = State()
    inline_id = State()
    user_msg_id = State()
    category = State()
    target = State()
    weekday = State()
    mode = State()
    target2 = State()
    time_start = State()
    time_end = State()
