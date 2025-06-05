from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message

from states import DeleteMenu, AddAdvertisement


class DeleteMenuMiddleware(BaseMiddleware):
    async def __call__(self,
                       handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
                       event: Message,
                       data: Dict[str, Any]) -> Any:
        state = data.get("state")
        res = await state.get_state()
        try:
            if res == DeleteMenu.menu_id:
                bot = data.get("bot")
                await bot.delete_message(event.chat.id, (await state.get_data()).get('menu_id'))
                await state.clear()

            elif res == AddAdvertisement.menu_id:
                bot = data.get("bot")
                await bot.delete_message(event.chat.id, (await state.get_data()).get('menu_id'))

                user_msg = (await state.get_data()).get('user_msg')
                if user_msg:
                    await bot.delete_message(event.chat.id, user_msg)

            elif res == AddAdvertisement.adding:
                pass

        except Exception as e:
            print(e)

        return await handler(event, data)
