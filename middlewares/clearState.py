from aiogram import BaseMiddleware
from aiogram.types import Message

from states import (DeleteMenu, AddAdvertisement, AddInformation, AddGroup, AddCoach, AddExercise, AddWorkout,
                    EditPassword)


class ClearStateMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: Message, data):
        state = data.get("state")

        result = await state.get_state()
        handler_name = data["handler"].callback.__name__

        if result == DeleteMenu.menu_id:
            await state.clear()

        elif result == AddAdvertisement.text and not handler_name == "advertisements_add":
            await state.clear()

        elif result == AddInformation.head and not handler_name == "information_add_head":
            await state.clear()

        elif result == AddInformation.text and not handler_name == "information_add_text":
            await state.clear()

        elif result == AddGroup.name and not handler_name == "groups_add_name":
            edit_group_id = (await state.get_data()).get("edit_group_id")
            await state.clear()
            await state.update_data(edit_group_id=edit_group_id)

        elif result == AddCoach.name and not handler_name == "coaches_add_name":
            edit_coach_id = (await state.get_data()).get("edit_coach_id")
            await state.clear()
            await state.update_data(edit_coach_id=edit_coach_id)

        elif result == AddExercise.head and not handler_name == "exercises_add_head":
            await state.clear()

        elif result == AddExercise.text and not handler_name == "exercises_add_text":
            await state.clear()

        elif result == AddWorkout.group_id:
            await state.clear()

        elif result == AddWorkout.exercise_id:
            await state.clear()

        elif result == AddWorkout.method and not handler_name == "workouts_add_method":
            await state.clear()

        elif result == EditPassword.new_password and not handler_name == "admins_edit_password_new":
            await state.clear()

        return await handler(event, data)
