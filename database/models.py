from datetime import datetime, timezone, timedelta

from sqlalchemy import BigInteger, DateTime
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

engine = create_async_engine(url='sqlite+aiosqlite:///db.sqlite3')

async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    tg_id: Mapped[int] = mapped_column(BigInteger)
    is_admin: Mapped[bool] = mapped_column(default=False)
    pushing: Mapped[bool] = mapped_column(default=True)


class Advertisement(Base):
    __tablename__ = 'advertisements'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    text: Mapped[str] = mapped_column(nullable=False)
    dt: Mapped[DateTime] = mapped_column(DateTime(timezone=True),
                                         default=lambda: datetime.now(timezone(timedelta(hours=10), name="KHV")))


class Information(Base):
    __tablename__ = 'information'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    head: Mapped[str] = mapped_column(nullable=False)
    text: Mapped[str] = mapped_column(nullable=False)


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
