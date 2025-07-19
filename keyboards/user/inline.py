from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from database import requests as rq

admins_add_proof = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="❌", callback_data=f"admins_add-no"),
        InlineKeyboardButton(text="✅", callback_data=f"admins_add-yes")
    ]
])


async def advertisements(number: int):
    buttons = []
    count = await rq.cnt_advertisements()

    if not count == 1:
        if not number == 1:
            buttons.append(InlineKeyboardButton(text="⬅", callback_data=f"advertisements_left_{number}"))
        if not number == count:
            buttons.append(InlineKeyboardButton(text="➡", callback_data=f"advertisements_right_{number}"))

    return InlineKeyboardMarkup(inline_keyboard=[buttons])


def information(page: int, number: int):
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Назад 🔙", callback_data=f"information_back_{page}_{number}"),
        ]
    ])


async def workouts(number: int, group_id: int):
    buttons = []
    count = await rq.cnt_workouts(group_id)

    if not count == 1:
        if not number == 1:
            buttons.append(InlineKeyboardButton(text="⬅", callback_data=f"workouts_left_{group_id}_{number}"))
        if not number == count:
            buttons.append(InlineKeyboardButton(text="➡", callback_data=f"workouts_right_{group_id}_{number}"))

    return InlineKeyboardMarkup(inline_keyboard=[
        buttons,
        [
            InlineKeyboardButton(text="Назад 🔙", callback_data=f"workouts_back_{group_id}_{number}")
        ]
    ])
