from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, CallbackQuery

from states import (DeleteMenu, AddAdvertisement, AddInformation, AddGroup, AddCoach, AddExercise, AddWorkout,
                    EditPassword, AddAdmin, AddLesson)

state_data = [AddAdvertisement.text, AddInformation.head, AddInformation.text, AddGroup.name, AddCoach.name,
              AddExercise.head, AddExercise.text, AddWorkout.group_id, AddWorkout.exercise_id, AddWorkout.method,
              EditPassword.password, EditPassword.new_password, AddAdmin.name, AddLesson.time_start]
state_inline = [AddAdvertisement.inline_id, AddInformation.inline_id, AddGroup.inline_id, AddCoach.inline_id,
                AddExercise.inline_id, AddWorkout.inline_id, EditPassword.inline_id, AddAdmin.inline_id]

class DeleteMenuMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: TelegramObject, data):
        if isinstance(event, CallbackQuery):
            if all(el in ["left", "right", "information"] for el in event.data.split("_")[:2]):
                return await handler(event, data)

            elif all(el in ["left", "right", "exercises"] for el in event.data.split("_")[:2]):
                return await handler(event, data)

            elif event.data.split("_")[0] == "workouts" and event.data.split("_")[1] in ["groups", "exercises"]:
                return await handler(event, data)

            elif event.data.split("_")[0] == "schedule":
                return await handler(event, data)

        state = data.get("state")
        res = await state.get_state()
        messages_id = []

        if res == DeleteMenu.menu_id:
            messages_id = [
                (await state.get_data()).get('menu_id'),
                (await state.get_data()).get('inline_id')
            ]

        elif res in state_data:
            messages_id = [
                (await state.get_data()).get('menu_id'),
                (await state.get_data()).get('user_msg_id')
            ]

        elif res in state_inline:
            messages_id = [
                (await state.get_data()).get('menu_id'),
                (await state.get_data()).get('inline_id'),
                (await state.get_data()).get('user_msg_id')
            ]

        bot = data.get("bot")
        for msg_id in messages_id:
            if msg_id:
                try:
                    await bot.delete_message(event.from_user.id, msg_id)
                except:
                    pass

        return await handler(event, data)
