from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from database import requests as rq

schedule_category = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Группы", callback_data=f"schedule_groups")
    ],
    [
        InlineKeyboardButton(text="Тренеры", callback_data=f"schedule_coaches")
    ]
])


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


async def schedule_groups_page(target: str = None, weekday: str = None, mode: str = None):
    buttons = []
    groups_list = await rq.get_groups_page()
    cb_data = f"coaches_{target}_{weekday}_{mode}" if target else "groups"

    for group in groups_list:
        buttons.append([
            InlineKeyboardButton(text=group[1], callback_data=f"schedule_{cb_data}_{group[0]}")
        ])

    buttons.append([
        InlineKeyboardButton(text="Назад 🔙", callback_data=f"schedule_{cb_data}_back")
    ])

    return InlineKeyboardMarkup(inline_keyboard=buttons)


async def schedule_coaches_page(target: str = None, weekday: str = None, mode: str = None):
    buttons = []
    coaches_list = await rq.get_coaches_page()
    cb_data = f"groups_{target}_{weekday}_{mode}" if target else "coaches"

    for coach in coaches_list:
        data_name = coach[1].split()
        name = data_name[0] + " " + data_name[1][0] + "." + data_name[2][0] + "."
        buttons.append([
            InlineKeyboardButton(text=name, callback_data=f"schedule_{cb_data}_{coach[0]}")
        ])

    buttons.append([
        InlineKeyboardButton(text="Назад 🔙", callback_data=f"schedule_{cb_data}_back")
    ])

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def schedule_weekdays(category: str, target: str):
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Понедельник", callback_data=f"schedule_{category}_{target}_monday")
        ],
        [
            InlineKeyboardButton(text="Вторник", callback_data=f"schedule_{category}_{target}_tuesday")
        ],
        [
            InlineKeyboardButton(text="Среда", callback_data=f"schedule_{category}_{target}_wednesday")
        ],
        [
            InlineKeyboardButton(text="Четверг", callback_data=f"schedule_{category}_{target}_thursday")
        ],
        [
            InlineKeyboardButton(text="Пятница", callback_data=f"schedule_{category}_{target}_friday")
        ],
        [
            InlineKeyboardButton(text="Суббота", callback_data=f"schedule_{category}_{target}_saturday")
        ],
        [
            InlineKeyboardButton(text="Воскресенье", callback_data=f"schedule_{category}_{target}_sunday")
        ],
        [
            InlineKeyboardButton(text="Назад 🔙", callback_data=f"schedule_{category}_{target}_back")
        ]
    ])
