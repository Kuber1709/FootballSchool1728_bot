from aiogram.fsm.state import State, StatesGroup


class DeleteMenu(StatesGroup):
    menu_id = State()
