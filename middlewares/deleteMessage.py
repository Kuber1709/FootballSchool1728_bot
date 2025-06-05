from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message

class DeleteMessageMiddleware(BaseMiddleware):
    def __init__(self):
        self.flag = False

    async def __call__(self,
                       handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
                       event: Message,
                       data: Dict[str, Any]) -> Any:
        result = await handler(event, data)

        if not result is None:
            await event.delete()

        return result
