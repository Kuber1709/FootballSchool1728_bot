from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from database import requests as rq


class RegistrationMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: TelegramObject, data):
        await rq.set_user(event.from_user.id)

        return await handler(event, data)
