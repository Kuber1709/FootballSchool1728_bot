from aiogram.filters import BaseFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from states import AddAdvertisement, DeleteMenu


class UndoFilter(BaseFilter):
    async def __call__(self, message: Message, state: FSMContext) -> bool:
        return (message.text == "Отмена 🚫" and await state.get_state() in
                (AddAdvertisement.menu_id, AddAdvertisement.adding, DeleteMenu.menu_id))
