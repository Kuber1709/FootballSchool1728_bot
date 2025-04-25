from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

user_messages_router = Router()


@user_messages_router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('Привет, Юзер!')
