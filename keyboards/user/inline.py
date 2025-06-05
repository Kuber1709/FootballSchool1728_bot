from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from database import requests as rq


async def advertisements(number: int):
    buttons = []
    count = await rq.cnt_advertisements()

    if not count == 1:
        if not number == 1:
            buttons.append(InlineKeyboardButton(text="⬅", callback_data="advertisements_left_" + str(number)))
        if not number == count:
            buttons.append(InlineKeyboardButton(text="➡", callback_data="advertisements_right_" + str(number)))

    kb = InlineKeyboardMarkup(inline_keyboard=[buttons])
    return kb


async def info_page(page: int):
    buttons = []
    page_list = await rq.get_information_page(page)

    for number in range(1, len(page_list) + 1):
        buttons.append(
            [InlineKeyboardButton(text=page_list[number - 1][0], callback_data=f"information_{page}_{number}")])

    count = await rq.cnt_information()
    if count > 5:
        buttons.append([])
        if not page == 1:
            buttons[-1].append(InlineKeyboardButton(text="⬅", callback_data="information_left_" + str(page)))
        if not page == (count + 4) // 5:
            buttons[-1].append(InlineKeyboardButton(text="➡", callback_data="information_right_" + str(page)))

    kb = InlineKeyboardMarkup(inline_keyboard=buttons)
    return kb


async def info_back(page: int):
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="Назад 🔙", callback_data=f"information_back_{page}")]])
