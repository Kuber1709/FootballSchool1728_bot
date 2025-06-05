from sqlalchemy import select, delete
from sqlalchemy.sql.functions import count

from .models import User, Advertisement, Information
from .models import async_session


async def set_user(tg_id: int):
    async with async_session() as session:
        if not await session.scalar(select(User).where(User.tg_id == tg_id)):
            session.add(User(tg_id=tg_id))
            await session.commit()


async def is_admin(tg_id: int):
    async with async_session() as session:
        return await session.scalar(select(User.is_admin).where(User.tg_id == tg_id))


async def is_user(tg_id: int):
    async with async_session() as session:
        return not await session.scalar(select(User.is_admin).where(User.tg_id == tg_id))


async def add_advertisement(text: str):
    async with async_session() as session:
        session.add(Advertisement(text=text))
        await session.commit()


async def cnt_advertisements():
    async with async_session() as session:
        return await session.scalar(select(count(Advertisement.id)))


async def get_advertisement(number: int):
    async with async_session() as session:
        return (await session.execute(select(Advertisement.text, Advertisement.dt))).all()[number - 1]


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
        return (await session.execute(select(Information.head, Information.text))).all()[number - 1]
