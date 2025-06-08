from aiogram import Router, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

import keyboards as kb
import texts as txt
from database import requests as rq
from filters import CallbackPrefixFilter
from states import AddAdvertisement, DeleteMenu
from .shared import advertisements_show, json_to_entities

admin_callback_router = Router()


@admin_callback_router.callback_query(CallbackPrefixFilter("advertisements"))
async def advertisements(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()
    data = callback_query.data.split("_")[1:]
    mode, number = data[0], int(data[1])
    result = None

    if mode == "add-no":
        await state.clear()
        await state.set_state(AddAdvertisement.menu_id)

        result = await callback_query.message.answer(txt.admin.advertisements_add,
                                                     reply_markup=kb.admin.reply.advertisements_undo)

    elif mode == "add-yes":
        data = await state.get_data()
        await mailing(callback_query.bot, data.get("text"), data.get("entities"), data.get("file_id"), data.get("mode"))
        await rq.add_advertisement(data.get("text"), data.get("entities"), data.get("file_id"), data.get("mode"))
        await state.clear()
        await state.set_state(DeleteMenu.menu_id)

        result = await callback_query.message.answer(txt.admin.advertisements_add_complete,
                                                     reply_markup=kb.admin.inline.advertisements_ready())

    elif mode == "del-no":
        await state.clear()
        await state.set_state(DeleteMenu.menu_id)
        count = await rq.cnt_advertisements()

        if not count:
            result = await callback_query.message.answer(txt.admin.no_advertisements)

        else:
            number = min(number, count) if number > 0 else 1
            result = await advertisements_show(callback_query.message, number)

    elif mode == "del-yes":
        await state.clear()
        await state.set_state(DeleteMenu.menu_id)
        await rq.del_advertisement(number)

        result = await callback_query.message.answer(txt.admin.advertisements_del_complete,
                                                     reply_markup=kb.admin.inline.advertisements_ready(number))

    elif mode in ["left", "right", "ready", "delete"]:
        await state.set_state(DeleteMenu.menu_id)

        if mode == "ready":
            text = txt.admin.advertisements_del_complete if number else txt.admin.advertisements_add_complete
            await callback_query.message.answer(text, reply_markup=kb.admin.reply.advertisements_back)

        count = await rq.cnt_advertisements()

        if not count:
            result = await callback_query.message.answer(txt.admin.no_advertisements)

        elif mode == "delete":
            result = await callback_query.message.answer(txt.admin.advertisements_del_proof)

            number = min(number, count) if number > 0 else 1
            result_inline = await advertisements_show(callback_query.message, number,
                                                      kb.admin.inline.advertisements_del_proof(number))

            await state.update_data(inline_id=result_inline.message_id)

        else:
            if mode == "left":
                number = min(number - 1, count) if number > 1 else 1
            elif mode == "right":
                number = min(number + 1, count) if number > 0 else 1
            elif mode == "ready":
                number = (min(number, count) if number > 0 else 1) if number else 1

            result = await advertisements_show(callback_query.message, number)

    await state.update_data(menu_id=result.message_id)


async def mailing(bot: Bot, text: str, json_entities: str, file_id: str, mode: str):
    entities = json_to_entities(json_entities)
    users_id = await rq.get_users_id()

    for user_id in users_id:
        try:
            await bot.send_message(chat_id=user_id[0], text=txt.admin.mailing, parse_mode="Markdown")
            if mode == "text":
                await bot.send_message(chat_id=user_id[0], text=text, entities=entities)

            elif mode == "photo":
                await bot.send_photo(chat_id=user_id[0], photo=file_id, caption=text, caption_entities=entities)

            elif mode == "video":
                await bot.send_video(chat_id=user_id[0], video=file_id, caption=text, caption_entities=entities)

            elif mode == "document":
                await bot.send_document(chat_id=user_id[0], document=file_id, caption=text, caption_entities=entities)

            elif mode == "audio":
                await bot.send_audio(chat_id=user_id[0], audio=file_id, caption=text, caption_entities=entities)

            elif mode == "voice":
                await bot.send_voice(chat_id=user_id[0], voice=file_id, caption=text, caption_entities=entities)

            elif mode == "video_note":
                await bot.send_video_note(chat_id=user_id[0], video_note=file_id)

            elif mode == "sticker":
                await bot.send_sticker(chat_id=user_id[0], sticker=file_id)

            elif mode == "animation":
                await bot.send_animation(chat_id=user_id[0], animation=file_id)
        except:
            pass
