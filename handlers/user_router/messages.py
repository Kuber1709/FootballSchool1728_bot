from aiogram import Router, F
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

import keyboards as kb
import texts as txt
from config import Config
from database import requests as rq
from filters import UndoFilter
from states import DeleteMenu, AddAdmin
from .shared import advertisements_show

user_messages_router = Router()


@user_messages_router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(txt.user.start, reply_markup=kb.user.reply.main)


@user_messages_router.message(Command("menu"))
async def cmd_menu(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(txt.shared.menu, reply_markup=kb.user.reply.main)


@user_messages_router.message(F.text.startswith("/admin_password_"))
async def cmd_admins_password(message: Message, state: FSMContext):
    if not Config.is_password_correct(message.text.removeprefix("/admin_password_")):
        await message.delete()

    else:
        await state.clear()
        await state.set_state(AddAdmin.name)

        await message.answer(txt.user.admins_add, reply_markup=kb.shared.reply.undo)
        result = await message.answer(txt.user.admins_add_name)

        await state.update_data(menu_id=result.message_id)


@user_messages_router.message(UndoFilter("admins"))
async def admins_undo(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(message.text, reply_markup=kb.user.reply.main)


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


@user_messages_router.message(F.text == "Информация ℹ")
async def information(message: Message, state: FSMContext):
    await state.set_state(DeleteMenu.menu_id)
    count = await rq.cnt_information()

    await message.answer(message.text, reply_markup=kb.user.reply.back)

    if not count:
        result = await message.answer(txt.shared.no_information)

    else:
        result = await message.answer(txt.shared.information_heads,
                                      reply_markup=await kb.shared.inline.information_page())

    await state.update_data(menu_id=result.message_id)


@user_messages_router.message(F.text == "Домашние тренировки 🏃")
async def workouts(message: Message, state: FSMContext):
    await state.set_state(DeleteMenu.menu_id)
    count = await rq.cnt_groups()

    await message.answer(message.text, reply_markup=kb.user.reply.back)

    if not count:
        result = await message.answer(txt.shared.no_groups)

    else:
        result = await message.answer(txt.shared.groups_names,
                                      reply_markup=await kb.shared.inline.groups_page("workouts"))

    await state.update_data(menu_id=result.message_id)


@user_messages_router.message(F.text == "Расписание 🔔")
async def schedule(message: Message, state: FSMContext):
    await state.set_state(DeleteMenu.menu_id)

    await message.answer(message.text, reply_markup=kb.user.reply.back)

    result = await message.answer(txt.shared.schedule_category, reply_markup=kb.shared.inline.schedule_category)

    await state.update_data(menu_id=result.message_id)


@user_messages_router.message(StateFilter(AddAdmin.name))
async def admins_add_name(message: Message, state: FSMContext):
    if not message.text:
        result = await message.answer(txt.user.admins_add_name)

    else:
        await state.set_state(AddAdmin.inline_id)

        result = await message.answer(text=txt.user.admins_add_proof)
        res = await message.answer(text=message.text, reply_markup=kb.user.inline.admins_add_proof)

        await state.update_data(name=message.text, inline_id=res.message_id)

    await state.update_data(menu_id=result.message_id, user_msg_id=message.message_id)
