from aiogram.fsm.state import StatesGroup, State


class AddAdmin(StatesGroup):
    menu_id = State()
    user_msg_id = State()
    inline_id = State()
    name = State()
