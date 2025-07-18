from aiogram.fsm.state import StatesGroup, State


class AddWorkout(StatesGroup):
    menu_id = State()
    inline_id = State()
    user_msg_id = State()
    group_id = State()
    exercise_id = State()
    method = State()
    entities = State()
