from aiogram.fsm.state import State, StatesGroup


class AddAdvertisement(StatesGroup):
    menu_id = State()
    adding = State()
    user_msg = State()
    text = State()
    file_id = State()
    entities = State()
    mode = State()
