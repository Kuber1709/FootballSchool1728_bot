from datetime import date, timedelta, datetime

from aiogram import Router, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, ReplyKeyboardRemove

import keyboards as kb
import texts as txt
from config import Config
from database import requests as rq
from filters import CallbackPrefixFilter
from states import (AddAdvertisement, DeleteMenu, AddInformation, AddGroup, AddCoach, AddExercise, AddWorkout,
                    EditPassword)
from .shared import json_to_entities, advertisements_show, information_show, exercises_show, workouts_show, admins_show

admin_callback_router = Router()

weekdays = {
    "monday": "Понедельник",
    "tuesday": "Вторник",
    "wednesday": "Среда",
    "thursday": "Четверг",
    "friday": "Пятница",
    "saturday": "Суббота",
    "sunday": "Воскресенье"
}


@admin_callback_router.callback_query(CallbackPrefixFilter("advertisements"))
async def advertisements(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()
    data = callback_query.data.split("_")[1:]
    mode, number = data[0], int(data[1])

    if mode in ["add-no", "del-no", "del-yes"]:
        await state.clear()

    if mode == "add-no":
        await state.set_state(AddAdvertisement.text)

        result = await callback_query.message.answer(txt.admin.advertisements_add)

    elif mode == "add-yes":
        data = await state.get_data()
        await mailing(callback_query.bot, data.get("text"), data.get("entities"), data.get("file_id"), data.get("mode"))
        await rq.add_advertisement(data.get("text"), data.get("entities"), data.get("file_id"), data.get("mode"))
        await state.clear()
        await state.set_state(DeleteMenu.menu_id)

        result = await callback_query.message.answer(txt.admin.advertisements_add_complete,
                                                     reply_markup=ReplyKeyboardRemove())
        await result.delete()
        result = await callback_query.message.answer(txt.admin.advertisements_add_complete,
                                                     reply_markup=kb.admin.inline.ready(mode="advertisements"))

    elif mode == "del-yes":
        await state.set_state(DeleteMenu.menu_id)
        await rq.del_advertisement(number)

        result = await callback_query.message.answer(txt.admin.advertisements_del_complete,
                                                     reply_markup=kb.admin.inline.ready(mode="advertisements",
                                                                                        num=number))

    else:
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
            result_inline = await advertisements_show(callback_query.message, number, mode == "delete")

            await state.update_data(inline_id=result_inline.message_id)

        else:
            if mode == "left":
                number = min(number - 1, count) if number > 1 else 1

            elif mode == "right":
                number = min(number + 1, count) if number > 0 else 1

            elif mode in ["ready", "del-no"]:
                number = min(number, count) if number > 0 else 1

            result = await advertisements_show(callback_query.message, number)

    await state.update_data(menu_id=result.message_id)


@admin_callback_router.callback_query(CallbackPrefixFilter("information"))
async def information(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()
    data = callback_query.data.split("_")[1:]
    mode, page = data[0], int(data[1])

    if mode in ["delete", "del-yes", "del-no", "add-no", "back"]:
        await state.clear()

    if mode == "add-no":
        await state.set_state(AddInformation.head)

        result = await callback_query.message.answer(txt.admin.information_add_head)

    elif mode == "add-yes":
        data = await state.get_data()
        await rq.add_information(data.get("head"), data.get("text"), data.get("entities"), data.get("file_id"),
                                 data.get("mode"))
        await state.clear()
        await state.set_state(DeleteMenu.menu_id)

        result = await callback_query.message.answer(txt.admin.information_add_complete,
                                                     reply_markup=ReplyKeyboardRemove())
        await result.delete()
        result = await callback_query.message.answer(txt.admin.information_add_complete,
                                                     reply_markup=kb.admin.inline.ready(mode="information"))

    elif mode == "del-yes":
        await state.set_state(DeleteMenu.menu_id)
        await rq.del_information((page - 1) * 5 + int(data[2]))

        result = await callback_query.message.answer(txt.admin.information_del_complete,
                                                     reply_markup=kb.admin.inline.ready(mode="information", num=page))

    else:
        await state.set_state(DeleteMenu.menu_id)

        if mode == "ready":
            text = txt.admin.information_del_complete if page else txt.admin.information_add_complete
            await callback_query.message.answer(text, reply_markup=kb.admin.reply.information_back)

        count = await rq.cnt_information()

        if not count:
            result = await callback_query.message.answer(txt.admin.no_information)

        elif mode in ["ready", "back"]:
            page = 1 if page < 1 else min(page, (count + 4) // 5)
            result = await callback_query.message.answer(txt.admin.information_heads,
                                                         reply_markup=await kb.admin.inline.information_page(page))

        elif mode in ["show", "delete", "del-no"]:
            result, result_inline = await information_show(callback_query.message, page, int(data[2]), mode == "delete")
            await state.update_data(inline_id=result_inline.message_id)

        else:
            if mode == "left":
                page = min(page - 1, (count + 4) // 5) if page > 1 else 1

            elif mode == "right":
                page = min(page + 1, (count + 4) // 5) if page > 0 else 1

            result = await callback_query.message.edit_text(txt.admin.information_heads,
                                                            reply_markup=await kb.admin.inline.information_page(page))

    await state.update_data(menu_id=result.message_id)


@admin_callback_router.callback_query(CallbackPrefixFilter("groups"))
async def groups(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()
    data = callback_query.data.split("_")[1:]
    mode, group_id = data[0], int(data[1])

    if mode in ["delete", "del-yes", "del-no", "back", "edit"]:
        await state.clear()

    if mode == "add-no":
        edit_group_id = (await state.get_data()).get("edit_group_id")
        await state.clear()
        await state.set_state(AddGroup.name)
        await state.update_data(edit_group_id=edit_group_id)

        result = await callback_query.message.answer(txt.admin.groups_add_name, reply_markup=None)

    elif mode == "add-yes":
        data = await state.get_data()
        edit_group_id, name = data.get("edit_group_id"), data.get("name")

        if edit_group_id:
            await rq.edit_group(edit_group_id, name)
            text = txt.admin.groups_edit_complete

        else:
            await rq.add_group(name)
            text = txt.admin.groups_add_complete

        await state.clear()
        await state.set_state(DeleteMenu.menu_id)
        await state.update_data(edit_group_id=edit_group_id)

        result = await callback_query.message.answer(text, reply_markup=ReplyKeyboardRemove())
        await result.delete()
        result = await callback_query.message.answer(text, reply_markup=kb.admin.inline.ready(mode="groups"))

    elif mode == "del-yes":
        await state.set_state(DeleteMenu.menu_id)
        await rq.del_group(group_id)

        result = await callback_query.message.answer(txt.admin.groups_del_complete,
                                                     reply_markup=kb.admin.inline.ready(mode="groups", num=group_id))

    elif mode == "edit":
        await state.set_state(AddGroup.name)

        result = await callback_query.message.answer(txt.admin.groups_add_name, reply_markup=kb.admin.reply.undo)

        await state.update_data(menu_id=result.message_id, edit_group_id=group_id)

    else:
        await state.set_state(DeleteMenu.menu_id)

        if mode == "ready":
            if (await state.get_data()).get("edit_group_id"):
                text = txt.admin.groups_edit_complete
            else:
                text = txt.admin.groups_del_complete if group_id else txt.admin.groups_add_complete
            await callback_query.message.answer(text, reply_markup=kb.admin.reply.groups_back)

        count = await rq.cnt_groups()

        if not count:
            result = await callback_query.message.answer(txt.admin.no_groups)

        elif mode in ["ready", "back"]:
            result = await callback_query.message.answer(txt.admin.groups_names,
                                                         reply_markup=await kb.admin.inline.groups_page())

        elif mode == "delete":
            result = await callback_query.message.answer(txt.admin.groups_del_proof)

            result_inline = await callback_query.message.answer(text=await rq.get_group(group_id),
                                                                reply_markup=kb.admin.inline.groups_del_proof(group_id))

            await state.update_data(inline_id=result_inline.message_id)

        else:
            result = await callback_query.message.answer(text=await rq.get_group(group_id),
                                                         reply_markup=kb.admin.inline.group(group_id))

    await state.update_data(menu_id=result.message_id)


@admin_callback_router.callback_query(CallbackPrefixFilter("coaches"))
async def coaches(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()
    data = callback_query.data.split("_")[1:]
    mode, coach_id = data[0], int(data[1])

    if mode in ["delete", "del-yes", "del-no", "back", "edit"]:
        await state.clear()

    if mode == "add-no":
        edit_coach_id = (await state.get_data()).get("edit_coach_id")
        await state.clear()
        await state.set_state(AddCoach.name)
        await state.update_data(edit_coach_id=edit_coach_id)

        result = await callback_query.message.answer(txt.admin.coaches_add_name)

    elif mode == "add-yes":
        data = await state.get_data()
        edit_coach_id, name = data.get("edit_coach_id"), data.get("name")

        if edit_coach_id:
            await rq.edit_coach(edit_coach_id, name)
            text = txt.admin.coaches_edit_complete

        else:
            await rq.add_coach(name)
            text = txt.admin.coaches_add_complete

        await state.clear()
        await state.set_state(DeleteMenu.menu_id)
        await state.update_data(edit_coach_id=edit_coach_id)

        result = await callback_query.message.answer(text, reply_markup=ReplyKeyboardRemove())
        await result.delete()
        result = await callback_query.message.answer(text, reply_markup=kb.admin.inline.ready(mode="coaches"))

    elif mode == "del-yes":
        await state.set_state(DeleteMenu.menu_id)
        await rq.del_coach(coach_id)

        result = await callback_query.message.answer(txt.admin.coaches_del_complete,
                                                     reply_markup=kb.admin.inline.ready(mode="coaches", num=coach_id))

    elif mode == "edit":
        await state.set_state(AddCoach.name)

        result = await callback_query.message.answer(txt.admin.coaches_add_name, reply_markup=kb.admin.reply.undo)

        await state.update_data(menu_id=result.message_id, edit_coach_id=coach_id)

    else:
        await state.set_state(DeleteMenu.menu_id)

        if mode == "ready":
            if (await state.get_data()).get("edit_coach_id"):
                text = txt.admin.coaches_edit_complete
            else:
                text = txt.admin.coaches_del_complete if coach_id else txt.admin.coaches_add_complete
            await callback_query.message.answer(text, reply_markup=kb.admin.reply.coaches_back)

        count = await rq.cnt_coaches()

        if not count:
            result = await callback_query.message.answer(txt.admin.no_coaches)

        elif mode in ["ready", "back"]:
            result = await callback_query.message.answer(txt.admin.coaches_names,
                                                         reply_markup=await kb.admin.inline.coaches_page())

        elif mode == "delete":
            result = await callback_query.message.answer(txt.admin.coaches_del_proof)

            result_inline = await callback_query.message.answer(text=await rq.get_coach(coach_id),
                                                                reply_markup=kb.admin.inline.coaches_del_proof(
                                                                    coach_id))

            await state.update_data(inline_id=result_inline.message_id)

        else:
            result = await callback_query.message.answer(text=await rq.get_coach(coach_id),
                                                         reply_markup=kb.admin.inline.coach(coach_id))

    await state.update_data(menu_id=result.message_id)


@admin_callback_router.callback_query(CallbackPrefixFilter("exercises"))
async def exercises(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()
    data = callback_query.data.split("_")[1:]
    mode, page = data[0], int(data[1])

    if mode in ["delete", "del-yes", "del-no", "add-no", "back"]:
        await state.clear()

    if mode == "add-no":
        await state.set_state(AddExercise.head)

        result = await callback_query.message.answer(txt.admin.exercises_add_head)

    elif mode == "add-yes":
        data = await state.get_data()
        await rq.add_exercise(data.get("head"), data.get("text"), data.get("entities"), data.get("file_id"),
                              data.get("mode"))
        await state.clear()
        await state.set_state(DeleteMenu.menu_id)

        result = await callback_query.message.answer(txt.admin.exercises_add_complete,
                                                     reply_markup=ReplyKeyboardRemove())
        await result.delete()
        result = await callback_query.message.answer(txt.admin.exercises_add_complete,
                                                     reply_markup=kb.admin.inline.ready(mode="exercises"))

    elif mode == "del-yes":
        await state.set_state(DeleteMenu.menu_id)

        await rq.del_exercise((page - 1) * 5 + int(data[2]))

        result = await callback_query.message.answer(txt.admin.exercises_del_complete,
                                                     reply_markup=kb.admin.inline.ready(mode="exercises", num=page))

    else:
        await state.set_state(DeleteMenu.menu_id)

        if mode == "ready":
            text = txt.admin.exercises_del_complete if page else txt.admin.exercises_add_complete
            await callback_query.message.answer(text, reply_markup=kb.admin.reply.exercises_back)

        count = await rq.cnt_exercises()

        if not count:
            result = await callback_query.message.answer(txt.admin.no_exercises)

        elif mode in ["ready", "back"]:
            page = 1 if page < 1 else min(page, (count + 4) // 5)
            result = await callback_query.message.answer(txt.admin.exercises_heads,
                                                         reply_markup=await kb.admin.inline.exercises_page(page))

        elif mode in ["show", "delete", "del-no"]:
            result, result_inline = await exercises_show(callback_query.message, page, int(data[2]), mode == "delete")
            await state.update_data(inline_id=result_inline.message_id)

        else:
            if mode == "left":
                page = min(page - 1, (count + 4) // 5) if page > 1 else 1

            elif mode == "right":
                page = min(page + 1, (count + 4) // 5) if page > 0 else 1

            result = await callback_query.message.edit_text(txt.admin.exercises_heads,
                                                            reply_markup=await kb.admin.inline.exercises_page(page))

    await state.update_data(menu_id=result.message_id)


@admin_callback_router.callback_query(CallbackPrefixFilter("workouts"))
async def workouts(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()
    data = callback_query.data.split("_")[1:]
    mode = data[0]

    if mode == "groups":
        await state.set_state(AddWorkout.exercise_id)

        await callback_query.message.edit_text(txt.admin.workouts_exercises_heads,
                                               reply_markup=await kb.admin.inline.workouts_exercises_page())

        await state.update_data(group_id=int(data[2]))

    elif mode == "exercises":
        if data[1].isdigit():
            await state.set_state(AddWorkout.method)

            await callback_query.message.edit_text(txt.admin.workouts_add_method, reply_markup=None)

            await state.update_data(exercise_id=int(data[1]))

        else:
            count = await rq.cnt_exercises()

            if not count:
                await state.clear()
                await state.set_state(AddWorkout.group_id)
                await callback_query.message.edit_text(txt.admin.workouts_no_exercises, reply_markup=None)

            else:
                await state.set_state(AddWorkout.exercise_id)
                page = int(data[2])

                if data[1] == "left":
                    page = min(page - 1, (count + 4) // 5) if page > 1 else 1

                elif data[1] == "right":
                    page = min(page + 1, (count + 4) // 5) if page > 0 else 1

                await callback_query.message.edit_text(txt.admin.workouts_exercises_heads,
                                                       reply_markup=await kb.admin.inline.workouts_exercises_page(page))

    elif mode == "add-no":
        await state.clear()
        await state.set_state(AddWorkout.group_id)
        count_groups = await rq.cnt_groups()
        count_exercises = await rq.cnt_exercises()

        if not count_groups:
            result = await callback_query.message.answer(txt.admin.workouts_no_groups)

        elif not count_exercises:
            result = await callback_query.message.answer(txt.admin.workouts_no_exercises)

        else:
            result = await callback_query.message.answer(txt.admin.workouts_groups_names,
                                                         reply_markup=await kb.admin.inline.groups_page(
                                                             "workouts_groups"))

        await state.update_data(menu_id=result.message_id)

    elif mode == "add-yes":
        data = await state.get_data()
        group_name, exercise_head = await rq.get_group_and_exercise(data.get("group_id"), data.get("exercise_id"))

        if not group_name or not exercise_head:
            await state.clear()
            await state.set_state(DeleteMenu.menu_id)
            count = await rq.cnt_groups()

            await callback_query.message.answer(txt.admin.workouts_add_error, reply_markup=kb.admin.reply.workouts_back)

            if not count:
                result = await callback_query.message.answer(txt.admin.no_groups)

            else:
                result = await callback_query.message.answer(txt.admin.groups_names,
                                                             reply_markup=await kb.admin.inline.groups_page(
                                                                 "workouts_groups"))

        else:
            await rq.add_workout(group_id=data.get("group_id"), exercise_id=data.get("exercise_id"),
                                 method=data.get("method"), entities=data.get("entities"))
            await state.clear()
            await state.set_state(DeleteMenu.menu_id)

            result = await callback_query.message.answer(txt.admin.workouts_add_complete,
                                                         reply_markup=ReplyKeyboardRemove())
            await result.delete()
            result = await callback_query.message.answer(txt.admin.workouts_add_complete,
                                                         reply_markup=kb.admin.inline.ready(mode="workouts"))

        await state.update_data(menu_id=result.message_id)

    elif mode == "ready":
        await state.set_state(DeleteMenu.menu_id)
        text = txt.admin.workouts_add_complete if not int(data[1]) else txt.admin.workouts_del_complete
        await callback_query.message.answer(text, reply_markup=kb.admin.reply.workouts_back)

        if not int(data[1]):
            count = await rq.cnt_groups()

            if not count:
                result = await callback_query.message.answer(txt.admin.no_groups)

            else:
                result = await callback_query.message.answer(txt.admin.groups_names,
                                                             reply_markup=await kb.admin.inline.groups_page(
                                                                 "workouts"))

        else:
            group_id, number = int(data[1]), int(data[2])
            count = await rq.cnt_workouts(group_id=group_id)

            number = min(number, count) if number > 0 else 1

            result, result_inline = await workouts_show(callback_query.message, number, group_id)
            await state.update_data(inline_id=result_inline.message_id)

        await state.update_data(menu_id=result.message_id)

    elif mode == "back":
        await state.set_state(DeleteMenu.menu_id)
        count = await rq.cnt_groups()

        if not count:
            result = await callback_query.message.answer(txt.admin.no_groups)

        else:
            result = await callback_query.message.answer(txt.admin.groups_names,
                                                         reply_markup=await kb.admin.inline.groups_page("workouts"))

        await state.update_data(menu_id=result.message_id)

    elif mode == "del-yes":
        await state.set_state(DeleteMenu.menu_id)
        group_id, number = int(data[1]), int(data[2])
        await rq.del_workout(group_id=group_id, number=number)

        result = await callback_query.message.answer(txt.admin.workouts_del_complete,
                                                     reply_markup=kb.admin.inline.workouts_del_ready(group_id, number))

        await state.update_data(menu_id=result.message_id)

    elif mode in ["show", "left", "right", "delete", "del-no"]:
        await state.set_state(DeleteMenu.menu_id)
        group_id, number = int(data[1]), int(data[2])
        count = await rq.cnt_workouts(group_id=group_id)

        if not count:
            result = await callback_query.message.answer(txt.admin.no_workouts,
                                                         reply_markup=kb.admin.inline.back("workouts"))

        else:
            if mode == "left":
                number = min(number - 1, count) if number > 1 else 1

            elif mode == "right":
                number = min(number + 1, count) if number > 0 else 1

            elif mode in ["show", "del-no"]:
                number = min(number, count) if number > 0 else 1

            result, result_inline = await workouts_show(callback_query.message, number, group_id, mode == "delete")

            await state.update_data(inline_id=result_inline.message_id)

        await state.update_data(menu_id=result.message_id)


@admin_callback_router.callback_query(CallbackPrefixFilter("admins"))
async def admins(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()
    data = callback_query.data.split("_")[1:]
    mode = data[0]

    if mode in ["delete", "del-yes", "del-no", "password-edit-no", "back"]:
        await state.clear()

    if mode == "password-edit-no":
        await state.set_state(EditPassword.password)

        result = await callback_query.message.answer(txt.admin.admins_edit_password_proof)

    elif mode == "password-edit-yes":
        data = await state.get_data()
        Config.change_password(data.get("new_password"))
        await state.clear()
        await state.set_state(DeleteMenu.menu_id)

        result = await callback_query.message.answer(txt.admin.admins_edit_password_complete,
                                                     reply_markup=ReplyKeyboardRemove())
        await result.delete()
        result = await callback_query.message.answer(txt.admin.admins_edit_password_complete,
                                                     reply_markup=kb.admin.inline.ready(mode="admins"))

    elif mode == "del-yes":
        await state.set_state(DeleteMenu.menu_id)
        admin_id = int(data[1])
        await rq.del_admin(admin_id)

        result = await callback_query.message.answer(txt.admin.admins_del_complete,
                                                     reply_markup=kb.admin.inline.ready(mode="admins", num=admin_id))

    else:
        await state.set_state(DeleteMenu.menu_id)
        admin_id = int(data[1])

        if mode == "ready":
            text = txt.admin.admins_del_complete if admin_id else txt.admin.admins_edit_password_complete
            await callback_query.message.answer(text, reply_markup=kb.admin.reply.admins_back)

            result = await callback_query.message.answer(txt.admin.admins_names,
                                                         reply_markup=await kb.admin.inline.admins_page())

        elif mode == "back":
            if admin_id:
                result, _ = await admins_show(callback_query.message, admin_id)

            else:
                result = await callback_query.message.answer(txt.admin.admins_names,
                                                             reply_markup=await kb.admin.inline.admins_page())

        elif mode == "delete":
            count = await rq.cnt_admins()

            if count == 1:
                result = await callback_query.message.answer(txt.admin.admins_del_error,
                                                             reply_markup=await kb.admin.inline.back(
                                                                 "admins", admin_id))

            else:
                result, result_inline = await admins_show(callback_query.message, admin_id, mode == "delete")

                await state.update_data(inline_id=result_inline.message_id)

        else:
            result, _ = await admins_show(callback_query.message, admin_id)

    await state.update_data(menu_id=result.message_id)


@admin_callback_router.callback_query(CallbackPrefixFilter("schedule"))
async def schedule(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()
    data = callback_query.data.split("_")[1:]
    mode, category = data[0], data[1]
    result = None

    if len(data) == 2:
        if category == "groups":
            result = await callback_query.message.edit_text(txt.admin.groups_names,
                                                            reply_markup=await kb.admin.inline.schedule_groups_page(
                                                                mode
                                                            ))

        elif category == "coaches":
            result = await callback_query.message.edit_text(txt.admin.coaches_names,
                                                            reply_markup=await kb.admin.inline.schedule_coaches_page(
                                                                mode
                                                            ))

    elif len(data) == 3:
        target = data[2]

        if target == "back":
            result = await callback_query.message.edit_text(txt.admin.schedule_category,
                                                            reply_markup=kb.admin.inline.schedule_category(mode))

        elif mode == "show":
            today = date.today()
            week_dates = [today - timedelta(days=today.weekday()) + timedelta(days=i) for i in range(7)]

            result = await callback_query.message.edit_text(txt.admin.schedule_weekdays,
                                                            reply_markup=kb.admin.inline.schedule_dates(
                                                                mode, category, target, week_dates
                                                            ))

        elif mode == "edit":
            result = await callback_query.message.edit_text(txt.admin.schedule_weekdays,
                                                            reply_markup=kb.admin.inline.schedule_weekdays(
                                                                mode, category, target
                                                            ))

    elif len(data) == 4 or data[4] == "del-no":
        target, day = data[2], data[3]

        if day == "back":
            if category == "groups":
                result = await callback_query.message.edit_text(txt.admin.groups_names,
                                                                reply_markup=await kb.admin.inline.schedule_groups_page(
                                                                    mode
                                                                ))

            else:
                result = await callback_query.message.edit_text(txt.admin.coaches_names,
                                                                reply_markup=await kb.admin.inline.schedule_coaches_page(
                                                                    mode
                                                                ))

        elif day.startswith("left") or day.startswith("right"):
            control, day = day.split("-")
            day = datetime.strptime(day, "%d.%m.%Y").date()
            day += timedelta(days=1) if control == "right" else timedelta(days=-1)
            week_dates = [day - timedelta(days=day.weekday()) + timedelta(days=i) for i in range(7)]

            result = await callback_query.message.edit_text(txt.admin.schedule_weekdays,
                                                            reply_markup=kb.admin.inline.schedule_dates(
                                                                mode, category, target, week_dates
                                                            ))

        else:
            title = day

            if "." in day:
                day = datetime.strptime(day, "%d.%m.%Y").date()
                title = weekdays[day.strftime("%A").lower()] + " " + title + "\n\n"

                if category == "groups":
                    lessons = await rq.get_lessons(day.strftime("%A").lower(), day, group_id=int(target))

                else:
                    lessons = await rq.get_lessons(day.strftime("%A").lower(), day, coach_id=int(target))

            else:
                title = weekdays[day] + "\n\n"

                if category == "groups":
                    lessons = await rq.get_lessons(day, group_id=int(target))

                else:
                    lessons = await rq.get_lessons(day, coach_id=int(target))


            if category == "coaches":
                coach_name_data = (await rq.get_coach(int(target))).split()
                title = "*" + coach_name_data[0] + " " + coach_name_data[1][0] + "." + coach_name_data[2][0] + ".*\n" + title

            else:
                title = "*" + await rq.get_group(int(target)) + "*\n" + title

            texts = []
            for lesson in lessons:
                if category == "groups":
                    data_name = lesson[4].split()
                    name = data_name[0] + " " + data_name[1][0] + "." + data_name[2][0] + "."
                    texts.append(txt.admin.schedule_lesson_coach.substitute(
                        name=name,
                        time_start=lesson[1].strftime("%H:%M"),
                        time_end=lesson[2].strftime("%H:%M")
                    ))

                else:
                    texts.append(txt.admin.schedule_lesson_group.substitute(
                        name=lesson[3],
                        time_start=lesson[1].strftime("%H:%M"),
                        time_end=lesson[2].strftime("%H:%M")
                    ))

            result = await callback_query.message.edit_text(title + "\n\n".join(texts), parse_mode="Markdown",
                                                            reply_markup=kb.admin.inline.schedule_day(
                                                                mode, category, target, day
                                                            ))

    elif len(data) == 5:
        target, day, btn = data[2], data[3], data[4]

        if btn == "back":
            if mode == "show":
                today = date.today()
                week_dates = [today - timedelta(days=today.weekday()) + timedelta(days=i) for i in range(7)]

                result = await callback_query.message.edit_text(txt.admin.schedule_weekdays,
                                                                reply_markup=kb.admin.inline.schedule_dates(
                                                                    mode, category, target, week_dates
                                                                ))

            elif mode == "edit":
                result = await callback_query.message.edit_text(txt.admin.schedule_weekdays,
                                                                reply_markup=kb.admin.inline.schedule_weekdays(
                                                                    mode, category, target
                                                                ))

        elif btn == "delete":
            if mode == "show":
                pass

            elif mode == "edit":
                pass


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
