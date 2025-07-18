from aiogram.fsm.state import StatesGroup, State


class EditSchedule(StatesGroup):
    menu_id = State()
    user_msg_id = State()
    inline_id = State()


