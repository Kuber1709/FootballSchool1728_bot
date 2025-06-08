from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from database import requests as rq

advertisements_add_proof = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="❌", callback_data=f"advertisements_add-no_0"),
        InlineKeyboardButton(text="✅", callback_data=f"advertisements_add-yes_0")
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

    kb = InlineKeyboardMarkup(inline_keyboard=[
        buttons,
        [
            InlineKeyboardButton(text="🗑", callback_data=f"advertisements_delete_{number}")
        ]
    ])
    return kb


def advertisements_del_proof(number: int):
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="❌", callback_data=f"advertisements_del-no_{number}"),
            InlineKeyboardButton(text="✅", callback_data=f"advertisements_del-yes_{number}")
        ]
    ])


def advertisements_ready(number: int = 0):
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Готово", callback_data=f"advertisements_ready_{number}")
        ]
    ])
