from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message

class DeleteMessageMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: Message, data):
        result = await handler(event, data)

        if not result is None:
            await event.delete()

        return result
