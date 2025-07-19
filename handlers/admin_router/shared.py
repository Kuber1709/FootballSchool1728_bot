from aiogram.types import Message, MessageEntity

import keyboards as kb
import texts as txt
from database import requests as rq
from ..shared import json_to_entities, show


async def advertisements_show(message: Message, number: int = 1, delete: bool = False):
    text, json_entities, file_id, mode, dt = await rq.get_advertisement(number)

    offset = len(text.encode('utf-16-le')) // 2 + 2 if text else 0
    entities = json_to_entities(json_entities) if json_entities else []
    entities += [MessageEntity(type="italic", offset=offset, length=16)]
    dt = dt.strftime("%d.%m.%Y %H:%M")

    text = txt.shared.advertisements_text.substitute(text=text, dt=dt) if text else dt
    inline = kb.admin.inline.advertisements_del_proof(number) if delete else await kb.admin.inline.advertisements(
        number)

    return await show(message, text, entities, file_id, mode, inline)


async def information_show(message: Message, page: int, number: int, delete: bool):
    inline = kb.admin.inline.information_del_proof(page, number) if delete else kb.admin.inline.information(page,
                                                                                                            number)

    number += (page - 1) * 5
    count = await rq.cnt_information()
    number = min(number, count) if number > 0 else 1
    head, text, json_entities, file_id, mode = await rq.get_information(number)

    head = txt.admin.information_del_proof.substitute(head=head) if delete else head
    entities = json_to_entities(json_entities)

    return await message.answer(head), await show(message, text, entities, file_id, mode, inline)


async def exercises_show(message: Message, page: int, number: int, delete: bool):
    inline = kb.admin.inline.exercises_del_proof(page, number) if delete else kb.admin.inline.exercises(page, number)

    number += (page - 1) * 5
    count = await rq.cnt_exercises()
    number = min(number, count) if number > 0 else 1
    head, text, json_entities, file_id, mode = await rq.get_exercise(number)

    head = txt.admin.exercises_del_proof.substitute(head=head) if delete else head
    entities = json_to_entities(json_entities)

    return await message.answer(head), await show(message, text, entities, file_id, mode, inline)


async def workouts_show(message: Message, number: int, group_id: int, delete: bool = False):
    group_name, exercise, method = await rq.get_workout(group_id, number)

    head = exercise[0] if not delete else txt.admin.workouts_del_proof.substitute(head=exercise[0], name=group_name)
    text = exercise[1]

    offset = len(text.encode('utf-16-le')) // 2 + 2 if text else 0
    entities = json_to_entities(exercise[2]) if exercise[2] else []
    entities += [MessageEntity(type="bold", offset=offset, length=17)]
    method_entities = json_to_entities(method[1]) if method[1] else []
    for entity in method_entities:
        entity.offset += (offset + 18)
    entities += method_entities
    text = txt.shared.workouts_text.substitute(text=text, method_text=method[0])
    inline = kb.admin.inline.workouts_del_proof(number, group_id) if delete else await kb.admin.inline.workouts(
        number, group_id)

    result = await message.answer(head)
    result_inline = await show(message, text, entities, exercise[3], exercise[4], inline)

    return result, result_inline


async def admins_show(message: Message, admin_id: int, delete: bool = False):
    name, tg_id, dt = await rq.get_admin(admin_id)

    tg_id = str(tg_id)
    dt = dt.strftime("%d.%m.%Y %H:%M")
    text = txt.admin.admins_text.substitute(name=name, tg_id=tg_id, dt=dt)

    if delete:
        result = await message.answer(txt.admin.admins_del_proof)
        result_inline = await message.answer(text, reply_markup=kb.admin.inline.admins_del_proof(admin_id),
                                             parse_mode="HTML")

    else:
        result = await message.answer(text, reply_markup=kb.admin.inline.admin(admin_id), parse_mode="HTML")
        result_inline = None

    return result, result_inline
