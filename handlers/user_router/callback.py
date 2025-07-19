from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, ReplyKeyboardRemove

import keyboards as kb
import texts as txt
from database import requests as rq
from filters import CallbackPrefixFilter
from states import DeleteMenu, AddAdmin
from .shared import advertisements_show, information_show, workouts_show

user_callback_router = Router()


@user_callback_router.callback_query(CallbackPrefixFilter("advertisements"))
async def advertisements(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()
    data = callback_query.data.split("_")[1:]
    mode, number = data[0], int(data[1])

    await state.set_state(DeleteMenu.menu_id)

    count = await rq.cnt_advertisements()

    if not count:
        result = await callback_query.message.answer(txt.shared.no_advertisements)

    else:
        if mode == "left":
            number = min(number - 1, count) if number > 1 else 1

        elif mode == "right":
            number = min(number + 1, count) if number > 0 else 1

        result = await advertisements_show(callback_query.message, number)

    await state.update_data(menu_id=result.message_id)


@user_callback_router.callback_query(CallbackPrefixFilter("information"))
async def information(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()
    data = callback_query.data.split("_")[1:]
    mode, page = data[0], int(data[1])

    await state.set_state(DeleteMenu.menu_id)

    count = await rq.cnt_information()

    if not count:
        result = await callback_query.message.answer(txt.shared.no_information)

    elif mode == "back":
        page = 1 if page < 1 else min(page, (count + 4) // 5)
        result = await callback_query.message.answer(txt.shared.information_heads,
                                                     reply_markup=await kb.shared.inline.information_page(page))

    elif mode == "show":
        result, result_inline = await information_show(callback_query.message, page, int(data[2]))
        await state.update_data(inline_id=result_inline.message_id)

    else:
        if mode == "left":
            page = min(page - 1, (count + 4) // 5) if page > 1 else 1

        elif mode == "right":
            page = min(page + 1, (count + 4) // 5) if page > 0 else 1

        result = await callback_query.message.edit_text(txt.shared.information_heads,
                                                        reply_markup=await kb.shared.inline.information_page(page))

    await state.update_data(menu_id=result.message_id)


@user_callback_router.callback_query(CallbackPrefixFilter("workouts"))
async def workouts(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()
    data = callback_query.data.split("_")[1:]
    mode = data[0]

    await state.set_state(DeleteMenu.menu_id)

    if mode == "back":
        count = await rq.cnt_groups()

        if not count:
            result = await callback_query.message.answer(txt.shared.no_groups)

        else:
            result = await callback_query.message.answer(txt.shared.groups_names,
                                                         reply_markup=await kb.shared.inline.groups_page("workouts"))

        await state.update_data(menu_id=result.message_id)

    elif mode in ["show", "left", "right"]:
        group_id, number = int(data[1]), int(data[2])
        count = await rq.cnt_workouts(group_id=group_id)

        if not count:
            result = await callback_query.message.answer(txt.shared.no_workouts,
                                                         reply_markup=kb.shared.inline.back("workouts"))

        else:
            if mode == "left":
                number = min(number - 1, count) if number > 1 else 1

            elif mode == "right":
                number = min(number + 1, count) if number > 0 else 1

            elif mode == "show":
                number = min(number, count) if number > 0 else 1

            result, result_inline = await workouts_show(callback_query.message, number, group_id)

            await state.update_data(inline_id=result_inline.message_id)

        await state.update_data(menu_id=result.message_id)


@user_callback_router.callback_query(CallbackPrefixFilter("admins"))
async def admins(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()
    mode = callback_query.data.split("_")[1]

    if mode == "add-no":
        await state.clear()
        await state.set_state(AddAdmin.name)

        result = await callback_query.message.answer(txt.user.admins_add_name)

    else:
        data = await state.get_data()
        await rq.add_admin(callback_query.from_user.id, data.get("name"))

        await state.clear()
        await state.set_state(DeleteMenu.menu_id)

        result = await callback_query.message.answer(txt.user.admins_add_complete, reply_markup=ReplyKeyboardRemove())
        await result.delete()
        result = await callback_query.message.answer(txt.user.admins_add_complete, reply_markup=kb.admin.reply.main)

    await state.update_data(menu_id=result.message_id)
