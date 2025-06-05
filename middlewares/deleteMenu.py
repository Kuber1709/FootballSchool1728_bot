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

                menu_id = (await state.get_data()).get('menu_id')
                if menu_id:
                    await bot.delete_message(event.chat.id, menu_id)
                await state.clear()

            elif res == AddAdvertisement.menu_id:
                bot = data.get("bot")

                menu_id = (await state.get_data()).get('menu_id')
                if menu_id:
                    await bot.delete_message(event.chat.id, menu_id)

                user_msg_id = (await state.get_data()).get('user_msg_id')
                if user_msg_id:
                    await bot.delete_message(event.chat.id, user_msg_id)

            elif res == AddAdvertisement.adding:
                bot = data.get("bot")

                menu_id = (await state.get_data()).get('menu_id')
                if menu_id:
                    await bot.delete_message(event.chat.id, menu_id)

                user_msg_id = (await state.get_data()).get('user_msg_id')
                if user_msg_id:
                    await bot.delete_message(event.chat.id, user_msg_id)

                inline_id = (await state.get_data()).get('inline_id')
                if inline_id:
                    await bot.delete_message(event.chat.id, inline_id)

        except Exception as e:
            print(e)

        return await handler(event, data)
