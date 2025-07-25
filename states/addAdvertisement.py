from aiogram.fsm.state import StatesGroup, State


class AddAdvertisement(StatesGroup):
    menu_id = State()
    user_msg_id = State()
    inline_id = State()
    text = State()
    file_id = State()
    entities = State()
    mode = State()
