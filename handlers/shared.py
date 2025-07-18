import json

from aiogram.types import Message, MessageEntity, InlineKeyboardMarkup

import keyboards as kb
import texts as txt
from database import requests as rq


async def advertisements_show(message: Message, number: int = 1, delete: bool = False):
    text, json_entities, file_id, mode, dt = await rq.get_advertisement(number)

    offset = len(text.encode('utf-16-le')) // 2 + 2 if text else 0
    entities = json_to_entities(json_entities) if json_entities else []
    entities += [MessageEntity(type="italic", offset=offset, length=16)]
    dt = dt.strftime("%d.%m.%Y %H:%M")

    text = txt.admin.advertisements_text.substitute(text=text, dt=dt) if text else dt
    inline = kb.admin.inline.advertisements_del_proof(number) if delete else await kb.admin.inline.advertisements(
        number)

    return await show(message, text, entities, file_id, mode, inline)


async def show(message: Message, text: str, entities: list[MessageEntity], file_id: str, mode: str,
               inline: InlineKeyboardMarkup = None):
    result = None

    if mode == "text":
        result = await message.answer(text=text, entities=entities, reply_markup=inline)

    elif mode == "photo":
        result = await message.answer_photo(photo=file_id, caption=text, caption_entities=entities,
                                            reply_markup=inline)

    elif mode == "video":
        result = await message.answer_video(video=file_id, caption=text, caption_entities=entities,
                                            reply_markup=inline)

    elif mode == "document":
        result = await message.answer_document(document=file_id, caption=text, caption_entities=entities,
                                               reply_markup=inline)

    elif mode == "audio":
        result = await message.answer_audio(audio=file_id, caption=text, caption_entities=entities,
                                            reply_markup=inline)

    elif mode == "voice":
        result = await message.answer_voice(voice=file_id, caption=text, caption_entities=entities,
                                            reply_markup=inline)

    elif mode == "video_note":
        result = await message.answer_video_note(video_note=file_id, reply_markup=inline)

    elif mode == "sticker":
        result = await message.answer_sticker(sticker=file_id, reply_markup=inline)

    elif mode == "animation":
        result = await message.answer_animation(animation=file_id, reply_markup=inline)

    return result


def json_to_entities(json_entities):
    if json_entities:
        return list(map(lambda entity: MessageEntity(**entity), json.loads(json_entities)))
    else:
        return None
