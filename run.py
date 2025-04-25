import asyncio
import logging

from aiogram import Bot, Dispatcher

from config import Config
from handlers import router
from database.models import async_main

bot = Bot(token=Config.BOT_TOKEN)
dp = Dispatcher()


async def main():
    await async_main()
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Bot is disabled')
