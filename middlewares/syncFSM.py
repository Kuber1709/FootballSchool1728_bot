from aiogram import BaseMiddleware


class SyncFSMMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        if data.get("state"):
            data["raw_state"] = await (data.get("state")).get_state()

        return await handler(event, data)
