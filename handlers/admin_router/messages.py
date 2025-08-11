import json
from re import fullmatch
from datetime import datetime

from aiogram import Router, F
from aiogram.filters import CommandStart, Command, StateFilter, or_f
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ContentType, InlineKeyboardMarkup

import keyboards as kb
import texts as txt
from config import Config
from database import requests as rq
from filters import UndoFilter
from states import (DeleteMenu, AddAdvertisement, AddInformation, AddGroup, AddCoach, AddExercise, AddWorkout,
                    EditPassword, AddLesson)
from .shared import advertisements_show
from ..shared import weekdays

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

pattern = r'^([01]?[0-9]|2[0-3]):([0-5][0-9])-([01]?[0-9]|2[0-3]):([0-5][0-9])$'


@admin_messages_router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(txt.admin.start, reply_markup=kb.admin.reply.main)


@admin_messages_router.message(Command("menu"))
async def cmd_menu(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(txt.shared.menu, reply_markup=kb.admin.reply.main)


@admin_messages_router.message(F.text.startswith("/admin_password_"))
async def cmd_admins_password(message: Message, state: FSMContext):
    if Config.is_password_correct(message.text.removeprefix("/admin_password_")):
        await state.clear()
        await message.answer(txt.admin.password, reply_markup=kb.admin.reply.main)

    else:
        await message.delete()


@admin_messages_router.message(F.text == "Назад 🔙")
async def back(message: Message, state: FSMContext):
    await message.answer(message.text, reply_markup=kb.admin.reply.main)


@admin_messages_router.message(or_f(F.text == "Объявления 📢", UndoFilter("advertisements")))
async def advertisements(message: Message, state: FSMContext):
    await state.set_state(DeleteMenu.menu_id)
    count = await rq.cnt_advertisements()

    await message.answer(message.text, reply_markup=kb.admin.reply.advertisements_back)

    if not count:
        result = await message.answer(txt.shared.no_advertisements)

    else:
        result = await advertisements_show(message)

    await state.update_data(menu_id=result.message_id)


@admin_messages_router.message(F.text == "Создать объявление 📢")
async def advertisements_create(message: Message, state: FSMContext):
    await state.set_state(AddAdvertisement.text)

    await message.answer(message.text, reply_markup=kb.shared.reply.undo)
    result = await message.answer(txt.admin.advertisements_add)

    await state.update_data(menu_id=result.message_id)


@admin_messages_router.message(or_f(F.text == "Информация ℹ", UndoFilter("information")))
async def information(message: Message, state: FSMContext):
    await state.set_state(DeleteMenu.menu_id)
    count = await rq.cnt_information()

    await message.answer(message.text, reply_markup=kb.admin.reply.information_back)

    if not count:
        result = await message.answer(txt.shared.no_information)

    else:
        result = await message.answer(txt.shared.information_heads,
                                      reply_markup=await kb.shared.inline.information_page())

    await state.update_data(menu_id=result.message_id)


@admin_messages_router.message(F.text == "Добавить информацию ℹ")
async def information_add(message: Message, state: FSMContext):
    await state.set_state(AddInformation.head)

    await message.answer(message.text, reply_markup=kb.shared.reply.undo)
    result = await message.answer(txt.admin.information_add_head)

    await state.update_data(menu_id=result.message_id)


@admin_messages_router.message(or_f(F.text == "Группы 👥", UndoFilter("groups")))
async def groups(message: Message, state: FSMContext):
    await state.set_state(DeleteMenu.menu_id)
    count = await rq.cnt_groups()
    data = await state.get_data()
    group_id = data.get("edit_group_id")

    await message.answer(message.text, reply_markup=kb.admin.reply.groups_back)

    if group_id:
        result = await message.answer(text=await rq.get_group(group_id), reply_markup=kb.admin.inline.group(group_id))

    elif not count:
        result = await message.answer(txt.shared.no_groups)

    else:
        result = await message.answer(txt.shared.groups_names, reply_markup=await kb.shared.inline.groups_page())

    await state.update_data(menu_id=result.message_id)


@admin_messages_router.message(F.text == "Добавить группу 👥")
async def groups_add(message: Message, state: FSMContext):
    await state.set_state(AddGroup.name)

    await message.answer(message.text, reply_markup=kb.shared.reply.undo)
    result = await message.answer(txt.admin.groups_add_name)

    await state.update_data(menu_id=result.message_id)


@admin_messages_router.message(or_f(F.text == "Тренеры 👤", UndoFilter("coaches")))
async def coaches(message: Message, state: FSMContext):
    await state.set_state(DeleteMenu.menu_id)
    count = await rq.cnt_coaches()
    data = await state.get_data()
    coach_id = data.get("edit_coach_id")

    await message.answer(message.text, reply_markup=kb.admin.reply.coaches_back)

    if coach_id:
        result = await message.answer(text=await rq.get_coach(coach_id), reply_markup=kb.admin.inline.coach(coach_id))

    elif not count:
        result = await message.answer(txt.shared.no_coaches)

    else:
        result = await message.answer(txt.shared.coaches_names, reply_markup=await kb.admin.inline.coaches_page())

    await state.update_data(menu_id=result.message_id)


@admin_messages_router.message(F.text == "Добавить тренера 👤")
async def coaches_add(message: Message, state: FSMContext):
    await state.set_state(AddCoach.name)

    await message.answer(message.text, reply_markup=kb.shared.reply.undo)
    result = await message.answer(txt.admin.coaches_add_name)

    await state.update_data(menu_id=result.message_id)


@admin_messages_router.message(or_f(F.text.in_(["Домашние тренировки 🏃", "Вернуться 🔙"]), UndoFilter("workouts")))
async def workouts(message: Message, state: FSMContext):
    await state.set_state(DeleteMenu.menu_id)
    count = await rq.cnt_groups()

    await message.answer(message.text, reply_markup=kb.admin.reply.workouts_back)

    if not count:
        result = await message.answer(txt.shared.no_groups)

    else:
        result = await message.answer(txt.shared.groups_names,
                                      reply_markup=await kb.shared.inline.groups_page("workouts"))

    await state.update_data(menu_id=result.message_id)


@admin_messages_router.message(F.text == "Добавить упражнение в тренировку 🏃")
async def workouts_add(message: Message, state: FSMContext):
    await state.set_state(AddWorkout.group_id)
    count_groups = await rq.cnt_groups()
    count_exercises = await rq.cnt_exercises()

    await message.answer(message.text, reply_markup=kb.shared.reply.undo)

    if not count_groups:
        result = await message.answer(txt.admin.workouts_no_groups)

    elif not count_exercises:
        result = await message.answer(txt.admin.workouts_no_exercises)

    else:
        result = await message.answer(txt.admin.workouts_groups_names,
                                      reply_markup=await kb.shared.inline.groups_page("workouts_groups"))

    await state.update_data(menu_id=result.message_id)


@admin_messages_router.message(or_f(F.text == "Упражнения ⚽", UndoFilter("exercises")))
async def exercises(message: Message, state: FSMContext):
    await state.set_state(DeleteMenu.menu_id)
    count = await rq.cnt_exercises()

    await message.answer(message.text, reply_markup=kb.admin.reply.exercises_back)

    if not count:
        result = await message.answer(txt.admin.no_exercises)

    else:
        result = await message.answer(txt.admin.exercises_heads, reply_markup=await kb.admin.inline.exercises_page())

    await state.update_data(menu_id=result.message_id)


@admin_messages_router.message(F.text == "Добавить упражнение ⚽")
async def exercises_add(message: Message, state: FSMContext):
    await state.set_state(AddExercise.head)

    await message.answer(message.text, reply_markup=kb.shared.reply.undo)
    result = await message.answer(txt.admin.exercises_add_head)

    await state.update_data(menu_id=result.message_id)


@admin_messages_router.message(or_f(F.text == "Админы 👨‍💻", UndoFilter("admins")))
async def admins(message: Message, state: FSMContext):
    await state.set_state(DeleteMenu.menu_id)

    await message.answer(message.text, reply_markup=kb.admin.reply.admins_back)

    result = await message.answer(txt.admin.admins_names, reply_markup=await kb.admin.inline.admins_page())

    await state.update_data(menu_id=result.message_id)


@admin_messages_router.message(F.text == "Добавить администратора 👨‍💻")
async def admins_add(message: Message, state: FSMContext):
    await state.set_state(EditPassword.password)

    await message.answer(message.text, reply_markup=kb.shared.reply.undo)
    result = await message.answer(txt.admin.admins_edit_password)

    await state.update_data(menu_id=result.message_id)


@admin_messages_router.message(F.text == "Расписание 🔔")
async def schedule(message: Message, state: FSMContext):
    await state.set_state(DeleteMenu.menu_id)

    await message.answer(message.text, reply_markup=kb.shared.reply.back)

    result = await message.answer(txt.shared.schedule_category, reply_markup=kb.shared.inline.schedule_category)

    await state.update_data(menu_id=result.message_id)


@admin_messages_router.message(StateFilter(AddAdvertisement.text))
async def advertisements_add(message: Message, state: FSMContext):
    if not message.content_type in media_types and not message.text:
        result = await message.answer(txt.admin.advertisements_add)

    else:
        await state.set_state(AddAdvertisement.inline_id)
        result = await message.answer(txt.admin.advertisements_add_proof)

        await message_save_data(message=message, state=state, inline=kb.admin.inline.advertisements_add_proof)

    await state.update_data(menu_id=result.message_id, user_msg_id=message.message_id)


@admin_messages_router.message(StateFilter(AddInformation.head))
async def information_add_head(message: Message, state: FSMContext):
    if not message.text:
        result = await message.answer(txt.admin.information_add_head)

    else:
        await state.set_state(AddInformation.text)
        await state.update_data(head=message.text)
        result = await message.answer(txt.admin.information_add_text)

    await state.update_data(menu_id=result.message_id, user_msg_id=message.message_id)


@admin_messages_router.message(StateFilter(AddInformation.text))
async def information_add_text(message: Message, state: FSMContext):
    if not message.content_type in media_types and not message.text:
        result = await message.answer(txt.admin.information_add_text)

    else:
        await state.set_state(AddInformation.inline_id)
        result = await message.answer(
            txt.admin.information_add_proof.substitute(head=(await state.get_data()).get("head")))

        await message_save_data(message=message, state=state, inline=kb.admin.inline.information_add_proof)

    await state.update_data(menu_id=result.message_id, user_msg_id=message.message_id)


@admin_messages_router.message(StateFilter(AddGroup.name))
async def groups_add_name(message: Message, state: FSMContext):
    if not message.text:
        result = await message.answer(txt.admin.groups_add_name)

    else:
        await state.set_state(AddGroup.inline_id)
        group_id = (await state.get_data()).get("edit_group_id")
        text = txt.admin.groups_edit_proof.substitute(
            name=await rq.get_group(group_id)) if group_id else txt.admin.groups_add_proof

        result = await message.answer(text=text)
        res = await message.answer(text=message.text, reply_markup=kb.admin.inline.groups_add_proof)

        await state.update_data(name=message.text, inline_id=res.message_id)

    await state.update_data(menu_id=result.message_id, user_msg_id=message.message_id)


@admin_messages_router.message(StateFilter(AddCoach.name))
async def coaches_add_name(message: Message, state: FSMContext):
    if not message.text:
        result = await message.answer(txt.admin.coaches_add_name)

    else:
        await state.set_state(AddCoach.inline_id)
        coach_id = (await state.get_data()).get("edit_coach_id")
        text = txt.admin.coaches_edit_proof.substitute(
            name=await rq.get_coach(coach_id)) if coach_id else txt.admin.coaches_add_proof

        result = await message.answer(text=text)
        res = await message.answer(text=message.text, reply_markup=kb.admin.inline.coaches_add_proof)

        await state.update_data(name=message.text, inline_id=res.message_id)

    await state.update_data(menu_id=result.message_id, user_msg_id=message.message_id)


@admin_messages_router.message(StateFilter(AddExercise.head))
async def exercises_add_head(message: Message, state: FSMContext):
    if not message.text:
        result = await message.answer(txt.admin.exercises_add_head)

    else:
        await state.set_state(AddExercise.text)
        await state.update_data(head=message.text)
        result = await message.answer(txt.admin.exercises_add_text)

    await state.update_data(menu_id=result.message_id, user_msg_id=message.message_id)


@admin_messages_router.message(StateFilter(AddExercise.text))
async def exercises_add_text(message: Message, state: FSMContext):
    if not message.content_type in media_types and not message.text:
        result = await message.answer(txt.admin.exercises_add_text)

    else:
        await state.set_state(AddExercise.inline_id)
        result = await message.answer(
            txt.admin.exercises_add_proof.substitute(head=(await state.get_data()).get("head")))

        await message_save_data(message=message, state=state, inline=kb.admin.inline.exercises_add_proof)

    await state.update_data(menu_id=result.message_id, user_msg_id=message.message_id)


@admin_messages_router.message(StateFilter(AddWorkout.method))
async def workouts_add_method(message: Message, state: FSMContext):
    if not message.text:
        result = await message.answer(txt.admin.workouts_add_method)

    else:
        data = await state.get_data()
        group_name, exercise_head = await rq.get_group_and_exercise(data.get("group_id"), data.get("exercise_id"))

        if not group_name or not exercise_head:
            await state.clear()
            await state.set_state(DeleteMenu.menu_id)
            count = await rq.cnt_groups()

            await message.delete()
            await message.answer(txt.admin.workouts_add_error, reply_markup=kb.admin.reply.workouts_back)

            if not count:
                result = await message.answer(txt.shared.no_groups)

            else:
                result = await message.answer(txt.shared.groups_names,
                                              reply_markup=await kb.shared.inline.groups_page("workouts_groups"))

        else:
            await state.set_state(AddWorkout.inline_id)

            result = await message.answer(txt.admin.workouts_add_proof.substitute(head=exercise_head, name=group_name))
            res = await message.answer(message.text, entities=message.entities,
                                       reply_markup=kb.admin.inline.workouts_add_proof)

            await state.update_data(method=message.text, entities=entities_to_json(message.entities),
                                    inline_id=res.message_id)

    await state.update_data(menu_id=result.message_id, user_msg_id=message.message_id)


@admin_messages_router.message(StateFilter(EditPassword.password))
async def admins_edit_password(message: Message, state: FSMContext):
    if not Config.is_password_correct(message.text):
        result = await message.answer(txt.admin.admins_edit_password_error)

    else:
        await state.set_state(EditPassword.new_password)

        result = await message.answer(txt.admin.admins_edit_password_new)

    await state.update_data(menu_id=result.message_id, user_msg_id=message.message_id)


@admin_messages_router.message(StateFilter(EditPassword.new_password))
async def admins_edit_password_new(message: Message, state: FSMContext):
    if not message.text or len(message.text) != len(message.text.encode('utf-16-le')) // 2:
        result = await message.answer(txt.admin.admins_edit_password_new)

    else:
        await state.set_state(EditPassword.inline_id)

        result = await message.answer(txt.admin.admins_edit_password_proof)
        result_inline = await message.answer(message.text, reply_markup=kb.admin.inline.admins_edit_password_proof)

        await state.update_data(new_password=message.text, inline_id=result_inline.message_id)

    await state.update_data(menu_id=result.message_id, user_msg_id=message.message_id)


@admin_messages_router.message(StateFilter(AddLesson.time_start))
async def schedule_add_time(message: Message, state: FSMContext):
    if not message.text or len(message.text) != len(message.text.encode('utf-16-le')) // 2:
        result = await message.answer(txt.admin.schedule_add_time, parse_mode="Markdown")

    elif not bool(fullmatch(pattern, message.text)):
        result = await message.answer(txt.admin.schedule_add_time, parse_mode="Markdown")

    else:
        await state.set_state(DeleteMenu.menu_id)
        data = await state.get_data()

        time_start = datetime.strptime(message.text.split("-")[0], "%H:%M").time()
        time_end = datetime.strptime(message.text.split("-")[1], "%H:%M").time()

        category = data.get("category")
        group = await rq.get_group(int(data.get("target" if category == "groups" else "target2")))
        coach_data = (await rq.get_coach(int(data.get("target2" if category == "groups" else "target")))).split()

        text = txt.admin.schedule_add_proof.substitute(
            weekday=weekdays[data.get("weekday")],
            coach=coach_data[0] + " " + coach_data[1][0] + "." + coach_data[2][0] + ".",
            group=group,
            time_start=time_start.strftime("%H:%M"),
            time_end=time_end.strftime("%H:%M")
        )

        result = await message.answer(text, parse_mode="Markdown",
                                      reply_markup=kb.admin.inline.schedule_add_proof(
                                          category, data.get("target"), data.get("weekday"), data.get("mode"),
                                          data.get("target2"), message.text
                                      ))

        await state.update_data(time_start=time_start, time_end=time_end)

    await state.update_data(menu_id=result.message_id, user_msg_id=message.message_id)


async def message_save_data(message: Message, state: FSMContext, inline: InlineKeyboardMarkup):
    result = None

    if message.text:
        result = await message.answer(
            text=message.text,
            entities=message.entities,
            reply_markup=inline
        )
        await state.update_data(text=result.text, entities=entities_to_json(result.entities), mode="text")

    elif message.photo:
        result = await message.answer_photo(
            photo=message.photo[-1].file_id,
            caption=message.caption,
            caption_entities=message.caption_entities,
            reply_markup=inline
        )
        await state.update_data(text=result.caption, entities=entities_to_json(result.caption_entities),
                                file_id=result.photo[-1].file_id, mode="photo")

    elif message.video:
        result = await message.answer_video(
            video=message.video.file_id,
            caption=message.caption,
            caption_entities=message.caption_entities,
            reply_markup=inline
        )
        await state.update_data(text=result.caption, entities=entities_to_json(result.caption_entities),
                                file_id=result.video.file_id, mode="video")

    elif message.document:
        result = await message.answer_document(
            document=message.document.file_id,
            caption=message.caption,
            caption_entities=message.caption_entities,
            reply_markup=inline
        )
        await state.update_data(text=result.caption, entities=entities_to_json(result.caption_entities),
                                file_id=result.document.file_id, mode="document")

    elif message.audio:
        result = await message.answer_audio(
            audio=message.audio.file_id,
            caption=message.caption,
            caption_entities=message.caption_entities,
            reply_markup=inline
        )
        await state.update_data(text=result.caption, entities=entities_to_json(result.caption_entities),
                                file_id=result.audio.file_id, mode="audio")

    elif message.voice:
        result = await message.answer_voice(
            voice=message.voice.file_id,
            caption=message.caption,
            caption_entities=message.caption_entities,
            reply_markup=inline
        )
        await state.update_data(text=result.caption, entities=entities_to_json(result.caption_entities),
                                file_id=result.voice.file_id, mode="voice", )

    elif message.video_note:
        result = await message.answer_video_note(
            video_note=message.video_note.file_id,
            reply_markup=inline
        )
        await state.update_data(file_id=result.video_note.file_id, mode="video_note")

    elif message.sticker:
        result = await message.answer_sticker(
            sticker=message.sticker.file_id,
            reply_markup=inline
        )
        await state.update_data(file_id=result.sticker.file_id, mode="sticker")

    elif message.animation:
        result = await message.answer_animation(
            animation=message.animation.file_id,
            reply_markup=inline
        )
        await state.update_data(file_id=result.animation.file_id, mode="animation")

    await state.update_data(inline_id=result.message_id)


def entities_to_json(entities):
    if entities:
        return json.dumps(list(map(vars, entities)))
    else:
        return None
