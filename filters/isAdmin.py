from aiogram.filters import BaseFilter
from aiogram.types import TelegramObject, Message, CallbackQuery

from database import requests as rq


class IsAdminFilter(BaseFilter):
    async def __call__(self, event: TelegramObject) -> bool:
        user_id = None

        if isinstance(event, Message):
            user_id = event.chat.id

        elif isinstance(event, CallbackQuery):
            user_id = event.from_user.id

        return await rq.is_admin(user_id)
