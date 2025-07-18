from aiogram.fsm.state import StatesGroup, State


class AddGroup(StatesGroup):
    menu_id = State()
    user_msg_id = State()
    inline_id = State()
    name = State()
    edit_group_id = State()
