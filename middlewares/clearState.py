from aiogram import BaseMiddleware
from aiogram.types import Message

from states import DeleteMenu, AddAdvertisement


class ClearStateMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: Message, data):
        state = data.get("state")
        result = await state.get_state()
        handler_name = data["handler"].callback.__name__

        conditions = [
            result == DeleteMenu.menu_id,
            all([
                result == AddAdvertisement.menu_id,
                not handler_name == "add_advertisement"
            ]),
            # result == AddAdvertisement.adding
        ]

        if any(conditions):
            await state.clear()

        return await handler(event, data)

