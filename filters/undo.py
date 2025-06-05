from aiogram.filters import BaseFilter
from aiogram.types import Message


from states import AddAdvertisement

class UndoFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return message.text == "Отмена 🚫" and (AddAdvertisement.menu_id or AddAdvertisement.adding)
