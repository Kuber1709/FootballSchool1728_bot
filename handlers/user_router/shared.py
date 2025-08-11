from aiogram.types import Message, MessageEntity

import keyboards as kb
import texts as txt
from database import requests as rq
from ..shared import json_to_entities, show


async def advertisements_show(message: Message, number: int = 1):
    text, json_entities, file_id, mode, dt = await rq.get_advertisement(number)

    offset = len(text.encode('utf-16-le')) // 2 + 2 if text else 0
    entities = json_to_entities(json_entities) if json_entities else []
    entities += [MessageEntity(type="italic", offset=offset, length=16)]
    dt = dt.strftime("%d.%m.%Y %H:%M")

    text = txt.shared.advertisements_text.substitute(text=text, dt=dt) if text else dt
    inline = await kb.user.inline.advertisements(number)

    return await show(message, text, entities, file_id, mode, inline)


async def information_show(message: Message, page: int, number: int):
    inline = kb.user.inline.information(page, number)

    number += (page - 1) * 5
    count = await rq.cnt_information()
    number = min(number, count) if number > 0 else 1
    head, text, json_entities, file_id, mode = await rq.get_information(number)

    entities = json_to_entities(json_entities)

    return await message.answer(head), await show(message, text, entities, file_id, mode, inline)


async def workouts_show(message: Message, number: int, group_id: int, ):
    group_name, exercise, method = await rq.get_workout(group_id, number)

    text = exercise[1]
    offset = len(text.encode('utf-16-le')) // 2 + 2 if text else 0

    entities = json_to_entities(exercise[2]) if exercise[2] else []
    entities += [MessageEntity(type="bold", offset=offset, length=17)]
    method_entities = json_to_entities(method[1]) if method[1] else []
    for entity in method_entities:
        entity.offset += (offset + 18)
    entities += method_entities

    text = txt.shared.workouts_text.substitute(text=text, method_text=method[0])
    inline = await kb.user.inline.workouts(number, group_id)

    result = await message.answer(exercise[0])
    result_inline = await show(message, text, entities, exercise[3], exercise[4], inline)

    return result, result_inline
