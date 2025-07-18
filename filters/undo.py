from aiogram.filters import BaseFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from states import (AddAdvertisement, AddInformation, AddGroup, AddCoach, AddExercise, AddWorkout, EditPassword,
                    EditSchedule)

advertisements = [AddAdvertisement.text, AddAdvertisement.inline_id]
information = [AddInformation.head, AddInformation.text, AddInformation.inline_id]
groups = [AddGroup.name, AddGroup.inline_id]
coaches = [AddCoach.name, AddCoach.inline_id]
exercises = [AddExercise.head, AddExercise.text, AddExercise.inline_id]
workouts = [AddWorkout.group_id, AddWorkout.exercise_id, AddWorkout.method, AddWorkout.inline_id]
admins = [EditPassword.password, EditPassword.new_password, EditPassword.inline_id]
schedule = [EditSchedule.menu_id]


class UndoFilter(BaseFilter):
    def __init__(self, mode: str):
        self.mode = mode

    async def __call__(self, message: Message, state: FSMContext) -> bool:
        if not message.text == "Отмена 🚫":
            return False

        result = await state.get_state()

        if self.mode == "advertisements" and result in advertisements:
            return True

        elif self.mode == "information" and result in information:
            return True

        elif self.mode == "groups" and result in groups:
            return True

        elif self.mode == "coaches" and result in coaches:
            return True

        elif self.mode == "exercises" and result in exercises:
            return True

        elif self.mode == "workouts" and result in workouts:
            return True

        elif self.mode == "admins" and result in admins:
            return True

        elif self.mode == "schedule" and result in schedule:
            return True

        else:
            return False
