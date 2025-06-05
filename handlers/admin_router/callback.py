from aiogram import Router
from aiogram.types import CallbackQuery

import keyboards as kb
import texts as txt
from database import requests as rq
from filters import CallbackPrefixFilter

admin_callback_router = Router()


@admin_callback_router.callback_query(CallbackPrefixFilter("advertisements"))
async def advertisements(callback_query: CallbackQuery):
    data = callback_query.data.split("_")[1:]
    mode, number = data[0], int(data[1])

    if mode == "delete":
        await callback_query.message.edit_text(txt.admin.advertisements_del_proof,
                                               reply_markup=await kb.admin.inline.advertisements_del_proof(number))
        return

    count = await rq.cnt_advertisements()

    if not count:
        await callback_query.message.edit_text(txt.admin.no_advertisements)

    else:
        if mode == "yes":
            await rq.del_advertisement(number)
            await callback_query.message.edit_text(txt.admin.advertisements_del,
                                                   reply_markup=await kb.admin.inline.advertisements_back(number))
            return

        new_number = None
        if mode == "no" or mode == "ready":
            new_number = min(number, count) if number > 0 else 1
        elif mode == "left":
            new_number = min(number - 1, count) if number > 1 else 1
        elif mode == "right":
            new_number = min(number + 1, count) if number > 0 else 1

        await callback_query.message.edit_text(await txt.admin.get_advertisement_text(new_number), parse_mode="Markdown",
                                               reply_markup=await kb.admin.inline.advertisements(new_number))