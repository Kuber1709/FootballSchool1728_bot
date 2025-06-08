import asyncio
from collections import defaultdict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject


class QueueMiddleware(BaseMiddleware):
    def __init__(self):
        self.user_queues = defaultdict(asyncio.Queue)
        self.active_workers = set()

    async def __call__(self, handler, event: TelegramObject, data):
        user_id = event.from_user.id
        await self.user_queues[user_id].put((handler, event, data))

        if user_id not in self.active_workers:
            self.active_workers.add(user_id)
            asyncio.create_task(self.process(user_id))

    async def process(self, user_id: int):
        while True:
            handler, event, data = await self.user_queues[user_id].get()

            await handler(event, data)

            self.user_queues[user_id].task_done()
            if self.user_queues[user_id].empty():
                self.active_workers.remove(user_id)
                break
