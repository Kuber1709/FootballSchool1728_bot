from aiogram.filters import BaseFilter
from aiogram.types import Message

from database import is_user


class IsUserFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return await is_user(message.chat.id)
