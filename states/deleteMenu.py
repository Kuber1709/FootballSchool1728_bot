from aiogram.fsm.state import StatesGroup, State


class DeleteMenu(StatesGroup):
    menu_id = State()
    inline_id = State()
