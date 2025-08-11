from datetime import datetime, timezone, timedelta, time

from sqlalchemy import BigInteger, DateTime, ForeignKey, Time
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

engine = create_async_engine(url='sqlite+aiosqlite:///db.sqlite3')

async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    tg_id: Mapped[int] = mapped_column(BigInteger, nullable=False)


class Admin(Base):
    __tablename__ = 'admins'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    tg_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)
    dt: Mapped[datetime] = mapped_column(DateTime(timezone=True),
                                         default=lambda: datetime.now(timezone(timedelta(hours=10), name="KHV")))


class Advertisement(Base):
    __tablename__ = 'advertisements'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    text: Mapped[str] = mapped_column(nullable=True)
    entities: Mapped[str] = mapped_column(nullable=True)
    file_id: Mapped[str] = mapped_column(nullable=True)
    mode: Mapped[str] = mapped_column(nullable=False)
    dt: Mapped[datetime] = mapped_column(DateTime(timezone=True),
                                         default=lambda: datetime.now(timezone(timedelta(hours=10), name="KHV")))


class Information(Base):
    __tablename__ = 'information'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    head: Mapped[str] = mapped_column(nullable=False)
    text: Mapped[str] = mapped_column(nullable=True)
    entities: Mapped[str] = mapped_column(nullable=True)
    file_id: Mapped[str] = mapped_column(nullable=True)
    mode: Mapped[str] = mapped_column(nullable=False)


class Coach(Base):
    __tablename__ = 'coaches'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False)

    lessons: Mapped[list["Lesson"]] = relationship(back_populates="coach", cascade="all, delete-orphan")


class Group(Base):
    __tablename__ = 'groups'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False)

    workouts: Mapped[list["Workout"]] = relationship(back_populates="group", cascade="all, delete-orphan")
    lessons: Mapped[list["Lesson"]] = relationship(back_populates="group", cascade="all, delete-orphan")


class Exercise(Base):
    __tablename__ = 'exercises'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    head: Mapped[str] = mapped_column(nullable=False)
    text: Mapped[str] = mapped_column(nullable=True)
    entities: Mapped[str] = mapped_column(nullable=True)
    file_id: Mapped[str] = mapped_column(nullable=True)
    mode: Mapped[str] = mapped_column(nullable=False)

    workouts: Mapped[list["Workout"]] = relationship(back_populates="exercise", cascade="all, delete-orphan")


class Workout(Base):
    __tablename__ = 'workouts'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    group_id: Mapped[int] = mapped_column(ForeignKey("groups.id", ondelete="CASCADE"))
    exercise_id: Mapped[int] = mapped_column(ForeignKey("exercises.id", ondelete="CASCADE"))
    method: Mapped[str] = mapped_column(nullable=False)
    entities: Mapped[str] = mapped_column(nullable=True)

    group: Mapped["Group"] = relationship(back_populates="workouts")
    exercise: Mapped["Exercise"] = relationship(back_populates="workouts")


class Lesson(Base):
    __tablename__ = 'lessons'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    weekday: Mapped[str] = mapped_column(nullable=False)
    group_id: Mapped[int] = mapped_column(ForeignKey("groups.id", ondelete="CASCADE"), nullable=False)
    coach_id: Mapped[int] = mapped_column(ForeignKey("coaches.id", ondelete="CASCADE"), nullable=False)
    time_start: Mapped[time] = mapped_column(Time(timezone=True), nullable=False)
    time_end: Mapped[time] = mapped_column(Time(timezone=True), nullable=False)

    group: Mapped["Group"] = relationship(back_populates="lessons")
    coach: Mapped["Coach"] = relationship(back_populates="lessons")


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
