from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

import keyboards as kb
import texts as txt
from database import requests as rq
from states import DeleteMenu

user_messages_router = Router()


@user_messages_router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(txt.user.start, reply_markup=kb.user.reply.main)


@user_messages_router.message(Command("menu"))
async def cmd_menu(message: Message):
    await message.answer(txt.user.menu, reply_markup=kb.user.reply.main)


@user_messages_router.message(F.text == "Назад 🔙")
async def back(message: Message):
    await message.answer(txt.user.back, reply_markup=kb.user.reply.main)


@user_messages_router.message(F.text == "Объявления 📢")
async def advertisements(message: Message, state: FSMContext):
    await state.set_state(DeleteMenu.menu_id)
    count = await rq.cnt_advertisements()

    await message.answer(txt.user.advertisements, reply_markup=kb.user.reply.back)

    if not count:
        result = await message.answer(txt.user.no_advertisements)

    else:
        result = await message.answer(await txt.user.get_advertisement_text(1), parse_mode="Markdown",
                                      reply_markup=await kb.user.inline.advertisements(1))

    await state.update_data(menu_id=result.message_id)


@user_messages_router.message(F.text == "Информация ℹ")
async def information(message: Message, state: FSMContext):
    await state.set_state(DeleteMenu.menu_id)
    count = await rq.cnt_information()

    await message.answer(txt.user.info, reply_markup=kb.user.reply.back)

    if not count:
        result = await message.answer(txt.user.no_information)

    else:
        result = await message.answer(txt.user.get_info, reply_markup=await kb.user.inline.info_page(1))

    await state.update_data(menu_id=result.message_id)
