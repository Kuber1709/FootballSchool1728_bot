from aiogram.fsm.state import StatesGroup, State


class AddInformation(StatesGroup):
    menu_id = State()
    inline_id = State()
    user_msg_id = State()
    head = State()
    text = State()
    entities = State()
    file_id = State()
    mode = State()
