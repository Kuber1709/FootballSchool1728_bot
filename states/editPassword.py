from aiogram.fsm.state import StatesGroup, State


class EditPassword(StatesGroup):
    menu_id = State()
    inline_id = State()
    user_msg_id = State()
    password = State()
    new_password = State()
