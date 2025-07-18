from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

import keyboards as kb
import texts as txt
from database import requests as rq
from states import DeleteMenu
from ..shared import

user_messages_router = Router()


@user_messages_router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(txt.user.start, reply_markup=kb.user.reply.main)


@user_messages_router.message(Command("menu"))
async def cmd_menu(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(txt.shared.menu, reply_markup=kb.user.reply.main)


@user_messages_router.message(F.text == "Назад 🔙")
async def back(message: Message):
    await message.answer(message.text, reply_markup=kb.user.reply.main)


@user_messages_router.message(F.text == "Объявления 📢")
async def advertisements(message: Message, state: FSMContext):
    await state.set_state(DeleteMenu.menu_id)
    count = await rq.cnt_advertisements()

    await message.answer(message.text, reply_markup=kb.user.reply.back)

    if not count:
        result = await message.answer(txt.shared.no_advertisements)

    else:
        result = await advertisements_show(message)

    await state.update_data(menu_id=result.message_id)
