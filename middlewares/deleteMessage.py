from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message, CallbackQuery


class DeleteMessageMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: TelegramObject, data):
        result = await handler(event, data)

        if not result is None:
            if isinstance(event, Message):
                await event.delete()

            elif isinstance(event, CallbackQuery):
                await event.message.delete()

        return result
