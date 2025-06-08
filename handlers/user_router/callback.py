from aiogram import Router
from aiogram.types import CallbackQuery

import keyboards as kb
import texts as txt
from database import requests as rq
from filters import CallbackPrefixFilter

user_callback_router = Router()


@user_callback_router.callback_query(CallbackPrefixFilter("advertisements_back"))
async def advertisements(callback_query: CallbackQuery):
    mode, number = callback_query.data.split("_")[1:]
    count = await rq.cnt_advertisements()

    if not count:
        await callback_query.message.edit_text(txt.user.no_advertisements, reply_markup=kb.user.reply.back)

    else:
        new_number = None
        if mode == "left":
            new_number = min(int(number) - 1, count) if int(number) > 1 else 1
        elif mode == "right":
            new_number = min(int(number) + 1, count) if int(number) > 0 else 1
        await callback_query.message.edit_text(await txt.user.get_advertisement_text(new_number), parse_mode="Markdown",
                                               reply_markup=await kb.user.inline.advertisements(new_number))


@user_callback_router.callback_query(CallbackPrefixFilter("information"))
async def information(callback_query: CallbackQuery):
    data = callback_query.data.split("_")[1:]
    count = await rq.cnt_information()

    if not count:
        await callback_query.message.edit_text(txt.user.no_information)

    else:
        if data[0].isdigit():
            page, number = int(data[0]), int(data[1])
            await callback_query.message.edit_text(await txt.user.get_information_text((page - 1) * 5 + number),
                                                   parse_mode="Markdown",
                                                   reply_markup=await kb.user.inline.info_back(page))

        else:
            mode, page = data[0], int(data[1])
            if mode == "back":
                await callback_query.message.edit_text(txt.user.get_info,
                                                       reply_markup=await kb.user.inline.info_page(page))

            else:
                new_page = None
                if mode == "left":
                    new_page = min(page - 1, (count + 4) // 5) if page > 1 else 1
                elif mode == "right":
                    new_page = min(page + 1, (count + 4) // 5) if page > 0 else 1
                await callback_query.message.edit_text(txt.user.get_info,
                                                       reply_markup=await kb.user.inline.info_page(new_page))
