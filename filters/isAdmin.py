from aiogram.filters import BaseFilter
from aiogram.types import Message

from database import is_admin


class IsAdminFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return await is_admin(message.chat.id)
