from datetime import time

from sqlalchemy import select, delete, update, text
from sqlalchemy.sql.functions import count

from .models import User, Admin, Advertisement, Information, Group, Coach, Exercise, Workout, Lesson
from .models import async_session


async def set_user(tg_id: int):
    async with async_session() as session:
        if not await session.scalar(select(User).where(User.tg_id == tg_id)):
            session.add(User(tg_id=tg_id))
            await session.commit()


async def get_users_id():
    async with async_session() as session:
        return (await session.execute(select(User.tg_id))).all()


async def is_admin(tg_id: int):
    async with async_session() as session:
        return await session.scalar(select(Admin.name).where(Admin.tg_id == tg_id))


async def is_user(tg_id: int):
    async with async_session() as session:
        return not await session.scalar(select(Admin.name).where(Admin.tg_id == tg_id))


async def add_advertisement(text: str, entities: str, file_id: str, mode: str):
    async with async_session() as session:
        session.add(Advertisement(text=text, entities=entities, file_id=file_id, mode=mode))
        await session.commit()


async def cnt_advertisements():
    async with async_session() as session:
        return await session.scalar(select(count(Advertisement.id)))


async def get_advertisement(number: int):
    async with async_session() as session:
        return (await session.execute(select(Advertisement.text, Advertisement.entities, Advertisement.file_id,
                                             Advertisement.mode, Advertisement.dt))).all()[::-1][number - 1]


async def del_advertisement(number: int):
    async with async_session() as session:
        a_id = (await session.execute(select(Advertisement.id))).all()[::-1][number - 1][0]
        await session.execute(delete(Advertisement).where(Advertisement.id == a_id))
        await session.commit()


async def cnt_information():
    async with async_session() as session:
        return await session.scalar(select(count(Information.id)))


async def get_information_page(page: int):
    async with async_session() as session:
        return (await session.execute(select(Information.head))).all()[
               5 * (page - 1):min(5 * page, await cnt_information())]


async def get_information(number: int):
    async with async_session() as session:
        return (await session.execute(select(Information.head, Information.text, Information.entities,
                                             Information.file_id, Information.mode))).all()[number - 1]


async def add_information(head: str, text: str, entities: str, file_id: str, mode: str):
    async with async_session() as session:
        session.add(Information(head=head, text=text, entities=entities, file_id=file_id, mode=mode))
        await session.commit()


async def del_information(number: int):
    async with async_session() as session:
        i_id = (await session.execute(select(Information.id))).all()[number - 1][0]
        await session.execute(delete(Information).where(Information.id == i_id))
        await session.commit()


async def cnt_groups():
    async with async_session() as session:
        return await session.scalar(select(count(Group.id)))


async def get_groups_page():
    async with async_session() as session:
        return (await session.execute(select(Group.id, Group.name))).all()


async def add_group(name: str):
    async with async_session() as session:
        session.add(Group(name=name))
        await session.commit()


async def edit_group(g_id: int, name: str):
    async with async_session() as session:
        await session.execute(update(Group).where(Group.id == g_id).values(name=name))
        await session.commit()


async def del_group(g_id: int):
    async with async_session() as session:
        await session.execute(delete(Group).where(Group.id == g_id))
        await session.commit()


async def get_group(g_id: int):
    async with async_session() as session:
        return await session.scalar(select(Group.name).where(Group.id == g_id))


async def cnt_coaches():
    async with async_session() as session:
        return await session.scalar(select(count(Coach.id)))


async def get_coaches_page():
    async with async_session() as session:
        return (await session.execute(select(Coach.id, Coach.name))).all()


async def add_coach(name: str):
    async with async_session() as session:
        session.add(Coach(name=name))
        await session.commit()


async def edit_coach(c_id: int, name: str):
    async with async_session() as session:
        await session.execute(update(Coach).where(Coach.id == c_id).values(name=name))
        await session.commit()


async def del_coach(c_id: int):
    async with async_session() as session:
        await session.execute(delete(Coach).where(Coach.id == c_id))
        await session.commit()


async def get_coach(c_id: int):
    async with async_session() as session:
        return await session.scalar(select(Coach.name).where(Coach.id == c_id))


async def cnt_exercises():
    async with async_session() as session:
        return await session.scalar(select(count(Exercise.id)))


async def get_exercises_page(page: int):
    async with async_session() as session:
        return (await session.execute(select(Exercise.head))).all()[
               5 * (page - 1):min(5 * page, await cnt_exercises())]


async def get_exercise(number: int):
    async with async_session() as session:
        return (await session.execute(select(Exercise.head, Exercise.text, Exercise.entities, Exercise.file_id,
                                             Exercise.mode))).all()[number - 1]


async def add_exercise(head: str, text: str, entities: str, file_id: str, mode: str):
    async with async_session() as session:
        session.add(Exercise(head=head, text=text, entities=entities, file_id=file_id, mode=mode))
        await session.commit()


async def del_exercise(number: int):
    async with async_session() as session:
        await session.execute(text("PRAGMA foreign_keys = ON"))
        e_id = (await session.execute(select(Exercise.id))).all()[number - 1][0]
        await session.execute(delete(Exercise).where(Exercise.id == e_id))
        await session.commit()


async def get_workouts_exercises(page: int):
    async with async_session() as session:
        return (await session.execute(select(Exercise.id, Exercise.head))).all()[
               5 * (page - 1):min(5 * page, await cnt_exercises())]


async def get_group_and_exercise(group_id: int, exercise_id: int):
    async with async_session() as session:
        group_name = await session.scalar(select(Group.name).where(Group.id == group_id))
        exercise_head = await session.scalar(select(Exercise.head).where(Exercise.id == exercise_id))
        return group_name, exercise_head


async def add_workout(group_id: int, exercise_id: int, method: str, entities: str):
    async with async_session() as session:
        session.add(Workout(group_id=group_id, exercise_id=exercise_id, method=method, entities=entities))
        await session.commit()


async def cnt_workouts(group_id: int):
    async with async_session() as session:
        return await session.scalar(select(count(Workout.id)).where(Workout.group_id == group_id))


async def del_workout(group_id: int, number: int):
    async with async_session() as session:
        w_id = (await session.execute(select(Workout.id).where(Workout.group_id == group_id))).all()[number - 1][0]
        await session.execute(delete(Workout).where(Workout.id == w_id))
        await session.commit()


async def get_workout(group_id: int, number: int):
    async with async_session() as session:
        method_text, method_entities, exercise_id = (await session.execute(
            select(Workout.method, Workout.entities, Workout.exercise_id)
            .where(Workout.group_id == group_id))
                                                     ).all()[number - 1]
        group_name = await get_group(group_id)
        exercise = (await session.execute(select(Exercise.head, Exercise.text, Exercise.entities, Exercise.file_id,
                                                 Exercise.mode).where(Exercise.id == exercise_id))).all()[0]

        return group_name, exercise, [method_text, method_entities]


async def cnt_admins():
    async with async_session() as session:
        return await session.scalar(select(count(Admin.id)))


async def get_admins_page():
    async with async_session() as session:
        return (await session.execute(select(Admin.id, Admin.name))).all()


async def add_admin(tg_id: int, name: str):
    async with async_session() as session:
        session.add(Admin(tg_id=tg_id, name=name))
        await session.commit()


async def del_admin(a_id: int):
    async with async_session() as session:
        await session.execute(delete(Admin).where(Admin.id == a_id))
        await session.commit()


async def get_admin(a_id: int):
    async with async_session() as session:
        return (await session.execute(select(Admin.name, Admin.tg_id, Admin.dt).where(Admin.id == a_id))).all()[0]


async def get_lessons(category: str, target: int, weekday: str):
    async with async_session() as session:
        return (await session.execute(
            select(Lesson.id, Lesson.time_start, Lesson.time_end, Group.name, Coach.name)
            .join(Group, Lesson.group_id == Group.id)
            .join(Coach, Lesson.coach_id == Coach.id)
            .where(Lesson.weekday == weekday)
            .where((Lesson.group_id if category == "groups" else Lesson.coach_id) == target)
            .order_by(Lesson.time_start))).all()


async def del_lesson(l_id: int):
    async with async_session() as session:
        await session.execute(delete(Lesson).where(Lesson.id == l_id))
        await session.commit()


async def add_lesson(weekday: str, coach_id: int, group_id: int, time_start: time, time_end: time):
    async with async_session() as session:
        session.add(Lesson(weekday=weekday, coach_id=coach_id, group_id=group_id, time_start=time_start,
                           time_end=time_end))
        await session.commit()
