from aiogram.fsm.state import StatesGroup, State


class AddCoach(StatesGroup):
    menu_id = State()
    user_msg_id = State()
    inline_id = State()
    name = State()
    edit_coach_id = State()
