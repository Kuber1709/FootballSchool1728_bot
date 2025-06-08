import json

from sqlalchemy import select, delete
from sqlalchemy.sql.functions import count

from .models import User, Advertisement, Information
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
        return await session.scalar(select(User.is_admin).where(User.tg_id == tg_id))


async def is_user(tg_id: int):
    async with async_session() as session:
        return not await session.scalar(select(User.is_admin).where(User.tg_id == tg_id))


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
                                             Advertisement.mode, Advertisement.dt))).all()[number - 1]


async def del_advertisement(number: int):
    async with async_session() as session:
        a_id = (await session.execute(select(Advertisement.id))).all()[number - 1][0]
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
