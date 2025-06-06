from aiogram import Router, F
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ContentType

import keyboards as kb
import texts as txt
from database import requests as rq
from filters import UndoFilter
from states import DeleteMenu, AddAdvertisement

admin_messages_router = Router()

media_types = {
    ContentType.PHOTO,
    ContentType.VIDEO,
    ContentType.DOCUMENT,
    ContentType.AUDIO,
    ContentType.VOICE,
    ContentType.VIDEO_NOTE,
    ContentType.STICKER,
    ContentType.ANIMATION
}


@admin_messages_router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(txt.admin.start, reply_markup=kb.admin.reply.main)


@admin_messages_router.message(Command("menu"))
async def cmd_menu(message: Message):
    await message.answer(txt.admin.menu, reply_markup=kb.admin.reply.main)


@admin_messages_router.message(F.text == "Назад 🔙")
async def back(message: Message):
    await message.answer(txt.admin.back, reply_markup=kb.admin.reply.main)


@admin_messages_router.message(F.text == "Объявления 📢")
async def advertisements(message: Message, state: FSMContext):
    await state.set_state(DeleteMenu.menu_id)
    count = await rq.cnt_advertisements()

    await message.answer(txt.admin.advertisements, reply_markup=kb.admin.reply.advertisements)

    if not count:
        result = await message.answer(txt.admin.no_advertisements)

    else:
        result = await message.answer(await txt.admin.get_advertisement_text(1), parse_mode="Markdown",
                                      reply_markup=await kb.admin.inline.advertisements(1))

    await state.update_data(menu_id=result.message_id)


@admin_messages_router.message(F.text == "Создать объявление 📢")
async def add_advertisement(message: Message, state: FSMContext):
    await state.set_state(AddAdvertisement.menu_id)

    await message.answer(txt.admin.advertisement_create, reply_markup=kb.admin.reply.undo)
    result = await message.answer(txt.admin.advertisement_add)

    await state.update_data(menu_id=result.message_id)


@admin_messages_router.message(UndoFilter())
async def undo_advertisement(message: Message, state: FSMContext):
    await state.set_state(DeleteMenu.menu_id)
    count = await rq.cnt_advertisements()

    await message.answer(txt.admin.advertisement_undo, reply_markup=kb.admin.reply.advertisements)

    if not count:
        result = await message.answer(txt.admin.no_advertisements)

    else:
        result = await message.answer(await txt.admin.get_advertisement_text(1), parse_mode="Markdown",
                                      reply_markup=await kb.admin.inline.advertisements(1))

    await state.update_data(menu_id=result.message_id)


@admin_messages_router.message(StateFilter(AddAdvertisement.menu_id))
async def add_advertisement(message: Message, state: FSMContext):
    if await state.get_state() == AddAdvertisement.adding:
        print("ppc")

    if not message.content_type in media_types and not message.text:
        result = await message.answer(txt.admin.advertisement_add)
        await state.update_data(menu_id=result.message_id, user_msg_id=message.message_id)
        return

    await state.set_state(AddAdvertisement.adding)
    result = await message.answer(txt.admin.advertisements_add_proof)

    if message.text:
        res = await message.answer(
            text=message.text,
            entities=message.entities,
            reply_markup=kb.admin.inline.advertisements_add_proof
        )
        await state.update_data(text=res.text, entities=res.entities, inline_id=res.message_id, mode="text",
                                menu_id=result.message_id, user_msg_id=message.message_id)

    elif message.photo:
        res = await message.answer_photo(
            photo=message.photo[-1].file_id,
            caption=message.caption,
            caption_entities=message.caption_entities,
            reply_markup=kb.admin.inline.advertisements_add_proof,
        )
        await state.update_data(text=res.caption, entities=res.caption_entities, file_id=res.photo[-1].file_id,
                                inline_id=res.message_id, mode="photo", menu_id=result.message_id,
                                user_msg_id=message.message_id)

    elif message.video:
        res = await message.answer_video(
            video=message.video.file_id,
            caption=message.caption,
            caption_entities=message.caption_entities,
            reply_markup=kb.admin.inline.advertisements_add_proof
        )
        await state.update_data(text=res.caption, entities=res.caption_entities, file_id=res.video.file_id,
                                inline_id=res.message_id, mode="video", menu_id=result.message_id,
                                user_msg_id=message.message_id)

    elif message.document:
        res = await message.answer_document(
            document=message.document.file_id,
            caption=message.caption,
            caption_entities=message.caption_entities,
            reply_markup=kb.admin.inline.advertisements_add_proof
        )
        await state.update_data(text=res.caption, entities=res.caption_entities, file_id=res.document.file_id,
                                inline_id=res.message_id, mode="document", menu_id=result.message_id,
                                user_msg_id=message.message_id)

    elif message.audio:
        res = await message.answer_audio(
            audio=message.audio.file_id,
            caption=message.caption,
            caption_entities=message.caption_entities,
            reply_markup=kb.admin.inline.advertisements_add_proof
        )
        await state.update_data(text=res.caption, entities=res.caption_entities, file_id=res.audio.file_id,
                                inline_id=res.message_id, mode="audio", menu_id=result.message_id,
                                user_msg_id=message.message_id)

    elif message.voice:
        res = await message.answer_voice(
            voice=message.voice.file_id,
            caption=message.caption,
            caption_entities=message.caption_entities,
            reply_markup=kb.admin.inline.advertisements_add_proof
        )
        await state.update_data(text=res.caption, entities=res.caption_entities, file_id=res.voice.file_id,
                                inline_id=res.message_id, mode="voice", menu_id=result.message_id,
                                user_msg_id=message.message_id)

    elif message.video_note:
        res = await message.answer_video_note(
            video_note=message.video_note.file_id,
            reply_markup=kb.admin.inline.advertisements_add_proof
        )
        await state.update_data(file_id=res.video_note.file_id, inline_id=res.message_id, mode="video_note",
                                menu_id=result.message_id, user_msg_id=message.message_id)

    elif message.sticker:
        res = await message.answer_sticker(
            sticker=message.sticker.file_id,
            reply_markup=kb.admin.inline.advertisements_add_proof
        )
        await state.update_data(file_id=res.sticker.file_id, inline_id=res.message_id, mode="sticker",
                                menu_id=result.message_id, user_msg_id=message.message_id)

    elif message.animation:
        res = await message.answer_animation(
            animation=message.animation.file_id,
            reply_markup=kb.admin.inline.advertisements_add_proof
        )
        await state.update_data(file_id=res.animation.file_id, inline_id=res.message_id, mode="animation",
                                menu_id=result.message_id, user_msg_id=message.message_id)
