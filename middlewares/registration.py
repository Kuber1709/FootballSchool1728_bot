from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from database import set_user

class RegistrationMiddleware(BaseMiddleware):
    async def __call__(self,
                 handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
                 event: TelegramObject,
                 data: Dict[str, Any]) -> Any:
        await set_user(data.get('event_from_user').id)
        return await handler(event, data)
