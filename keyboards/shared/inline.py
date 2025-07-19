from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from database import requests as rq


async def information_page(page: int = 1):
    buttons = []
    page_list = await rq.get_information_page(page)

    for number in range(1, len(page_list) + 1):
        buttons.append([
            InlineKeyboardButton(text=page_list[number - 1][0], callback_data=f"information_show_{page}_{number}")
        ])

    count = await rq.cnt_information()

    if count > 5:
        buttons.append([])

        if not page == 1:
            buttons[-1].append(InlineKeyboardButton(text="⬅", callback_data="information_left_" + str(page)))

        if not page == (count + 4) // 5:
            buttons[-1].append(InlineKeyboardButton(text="➡", callback_data="information_right_" + str(page)))

    return InlineKeyboardMarkup(inline_keyboard=buttons)


async def groups_page(title: str = "groups"):
    buttons = []
    groups_list = await rq.get_groups_page()

    for group in groups_list:
        buttons.append([
            InlineKeyboardButton(text=group[1], callback_data=f"{title}_show_{group[0]}_1")
        ])

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def back(title: str, num: int = 0):
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Назад 🔙", callback_data=f"{title}_back_{num}")
        ]
    ])
