from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from database import requests as rq

advertisements_add_proof = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="❌", callback_data=f"advertisements_add_no"),
        InlineKeyboardButton(text="✅", callback_data=f"advertisements_add_yes")
    ]
])


async def advertisements(number: int):
    buttons = []
    count = await rq.cnt_advertisements()

    if not count == 1:
        if not number == 1:
            buttons.append(InlineKeyboardButton(text="⬅", callback_data="advertisements_left_" + str(number)))
        if not number == count:
            buttons.append(InlineKeyboardButton(text="➡", callback_data="advertisements_right_" + str(number)))

    kb = InlineKeyboardMarkup(inline_keyboard=[
        buttons,
        [
            InlineKeyboardButton(text="🗑", callback_data=f"advertisements_delete_{number}")
        ]
    ])
    return kb


async def advertisements_del_proof(number: int):
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="❌", callback_data=f"advertisements_no_{number}"),
            InlineKeyboardButton(text="✅", callback_data=f"advertisements_yes_{number}")
        ]
    ])


async def advertisements_back(number: int):
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Готово", callback_data=f"advertisements_ready_{number}")
        ]
    ])
