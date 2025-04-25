from sqlalchemy import select

from .models import User
from .models import async_session


async def set_user(tg_id):
    async with async_session() as session:
        if not await session.scalar(select(User).where(User.tg_id == tg_id)):
            session.add(User(tg_id=tg_id))
            await session.commit()


async def is_admin(tg_id):
    async with async_session() as session:
        return await session.scalar(select(User.is_admin).where(User.tg_id == tg_id))


async def is_user(tg_id):
    async with async_session() as session:
        return not await session.scalar(select(User.is_admin).where(User.tg_id == tg_id))
