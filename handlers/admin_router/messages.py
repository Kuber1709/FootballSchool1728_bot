import json

from aiogram import Router, F
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ContentType

import keyboards as kb
import texts as txt
from database import requests as rq
from filters import UndoFilter
from states import DeleteMenu, AddAdvertisement
from .shared import advertisements_show

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

    await message.answer(txt.admin.advertisements, reply_markup=kb.admin.reply.advertisements_back)

    if not count:
        result = await message.answer(txt.admin.no_advertisements)

    else:
        result = await advertisements_show(message)

    await state.update_data(menu_id=result.message_id)


@admin_messages_router.message(F.text == "Создать объявление 📢")
async def advertisements_create(message: Message, state: FSMContext):
    await state.set_state(AddAdvertisement.menu_id)

    await message.answer(txt.admin.advertisements_create, reply_markup=kb.admin.reply.advertisements_undo)
    result = await message.answer(txt.admin.advertisements_add)

    await state.update_data(menu_id=result.message_id)


@admin_messages_router.message(UndoFilter())
async def advertisements_undo(message: Message, state: FSMContext):
    await state.set_state(DeleteMenu.menu_id)
    count = await rq.cnt_advertisements()

    await message.answer(txt.admin.advertisements_undo, reply_markup=kb.admin.reply.advertisements_back)

    if not count:
        result = await message.answer(txt.admin.no_advertisements)

    else:
        result = await advertisements_show(message)

    await state.update_data(menu_id=result.message_id)


@admin_messages_router.message(StateFilter(AddAdvertisement.menu_id))
async def advertisements_add(message: Message, state: FSMContext):
    if not message.content_type in media_types and not message.text:
        result = await message.answer(txt.admin.advertisements_add)

    else:
        await state.set_state(AddAdvertisement.adding)
        result = await message.answer(txt.admin.advertisements_add_proof)

        await advertisements_save_data(message=message, state=state)

    await state.update_data(menu_id=result.message_id, user_msg_id=message.message_id)


async def advertisements_save_data(message: Message, state: FSMContext):
    result = None

    if message.text:
        result = await message.answer(
            text=message.text,
            entities=message.entities,
            reply_markup=kb.admin.inline.advertisements_add_proof
        )
        await state.update_data(text=result.text, entities=entities_to_json(result.entities), mode="text")

    elif message.photo:
        result = await message.answer_photo(
            photo=message.photo[-1].file_id,
            caption=message.caption,
            caption_entities=message.caption_entities,
            reply_markup=kb.admin.inline.advertisements_add_proof
        )
        await state.update_data(text=result.caption, entities=entities_to_json(result.caption_entities),
                                file_id=result.photo[-1].file_id, mode="photo")

    elif message.video:
        result = await message.answer_video(
            video=message.video.file_id,
            caption=message.caption,
            caption_entities=message.caption_entities,
            reply_markup=kb.admin.inline.advertisements_add_proof
        )
        await state.update_data(text=result.caption, entities=entities_to_json(result.caption_entities),
                                file_id=result.video.file_id, mode="video")

    elif message.document:
        result = await message.answer_document(
            document=message.document.file_id,
            caption=message.caption,
            caption_entities=message.caption_entities,
            reply_markup=kb.admin.inline.advertisements_add_proof
        )
        await state.update_data(text=result.caption, entities=entities_to_json(result.caption_entities),
                                file_id=result.document.file_id, mode="document")

    elif message.audio:
        result = await message.answer_audio(
            audio=message.audio.file_id,
            caption=message.caption,
            caption_entities=message.caption_entities,
            reply_markup=kb.admin.inline.advertisements_add_proof
        )
        await state.update_data(text=result.caption, entities=entities_to_json(result.caption_entities),
                                file_id=result.audio.file_id, mode="audio")

    elif message.voice:
        result = await message.answer_voice(
            voice=message.voice.file_id,
            caption=message.caption,
            caption_entities=message.caption_entities,
            reply_markup=kb.admin.inline.advertisements_add_proof
        )
        await state.update_data(text=result.caption, entities=entities_to_json(result.caption_entities),
                                file_id=result.voice.file_id, mode="voice", )

    elif message.video_note:
        result = await message.answer_video_note(
            video_note=message.video_note.file_id,
            reply_markup=kb.admin.inline.advertisements_add_proof
        )
        await state.update_data(file_id=result.video_note.file_id, mode="video_note")

    elif message.sticker:
        result = await message.answer_sticker(
            sticker=message.sticker.file_id,
            reply_markup=kb.admin.inline.advertisements_add_proof
        )
        await state.update_data(file_id=result.sticker.file_id, mode="sticker")

    elif message.animation:
        result = await message.answer_animation(
            animation=message.animation.file_id,
            reply_markup=kb.admin.inline.advertisements_add_proof
        )
        await state.update_data(file_id=result.animation.file_id, mode="animation")

    await state.update_data(inline_id=result.message_id)


def entities_to_json(entities):
    if entities:
        return json.dumps(list(map(vars, entities)))
    else:
        return None
