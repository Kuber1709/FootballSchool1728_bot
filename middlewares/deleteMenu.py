from aiogram import BaseMiddleware
from aiogram.types import Message

from states import DeleteMenu, AddAdvertisement


class DeleteMenuMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: Message, data):
        state = data.get("state")
        res = await state.get_state()
        messages_id = []

        if res == DeleteMenu.menu_id:
            messages_id.append((await state.get_data()).get('menu_id'))

        elif res == AddAdvertisement.menu_id:
            messages_id.append((await state.get_data()).get('menu_id'))
            messages_id.append((await state.get_data()).get('user_msg_id'))

        elif res == AddAdvertisement.adding:
            messages_id.append((await state.get_data()).get('menu_id'))
            messages_id.append((await state.get_data()).get('user_msg_id'))
            messages_id.append((await state.get_data()).get('inline_id'))

        bot = data.get("bot")
        for msg_id in messages_id:
            if msg_id:
                try:
                    await bot.delete_message(event.chat.id, msg_id)
                except:
                    pass

        return await handler(event, data)
