from datetime import date
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from database import requests as rq

advertisements_add_proof = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="❌", callback_data=f"advertisements_add-no_0"),
        InlineKeyboardButton(text="✅", callback_data=f"advertisements_add-yes_0")
    ]
])

information_add_proof = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="❌", callback_data=f"information_add-no_0"),
        InlineKeyboardButton(text="✅", callback_data=f"information_add-yes_0")
    ]
])

groups_add_proof = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="❌", callback_data=f"groups_add-no_0"),
        InlineKeyboardButton(text="✅", callback_data=f"groups_add-yes_0")
    ]
])

coaches_add_proof = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="❌", callback_data=f"coaches_add-no_0"),
        InlineKeyboardButton(text="✅", callback_data=f"coaches_add-yes_0")
    ]
])

exercises_add_proof = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="❌", callback_data=f"exercises_add-no_0"),
        InlineKeyboardButton(text="✅", callback_data=f"exercises_add-yes_0")
    ]
])

workouts_add_proof = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="❌", callback_data=f"workouts_add-no_0"),
        InlineKeyboardButton(text="✅", callback_data=f"workouts_add-yes_0")
    ]
])

admins_edit_password_proof = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="❌", callback_data=f"admins_password-edit-no"),
        InlineKeyboardButton(text="✅", callback_data=f"admins_password-edit-yes")
    ]
])


def ready(mode: str, num: int = 0):
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Готово ✅", callback_data=f"{mode}_ready_{num}")
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


def information(page: int, number: int):
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🗑", callback_data=f"information_delete_{page}_{number}"),
        ],
        [
            InlineKeyboardButton(text="Назад 🔙", callback_data=f"information_back_{page}_{number}"),
        ]
    ])


def information_del_proof(page: int, number: int):
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="❌", callback_data=f"information_del-no_{page}_{number}"),
            InlineKeyboardButton(text="✅", callback_data=f"information_del-yes_{page}_{number}")
        ]
    ])


def group(g_id: int):
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🗑", callback_data=f"groups_delete_{g_id}"),
            InlineKeyboardButton(text="📝", callback_data=f"groups_edit_{g_id}")
        ],
        [
            InlineKeyboardButton(text="Назад 🔙", callback_data=f"groups_back_{g_id}"),
        ]
    ])


def groups_del_proof(g_id: int):
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="❌", callback_data=f"groups_del-no_{g_id}"),
            InlineKeyboardButton(text="✅", callback_data=f"groups_del-yes_{g_id}")
        ]
    ])


async def coaches_page():
    buttons = []
    coaches_list = await rq.get_coaches_page()

    for coach in coaches_list:
        data_name = coach[1].split()
        name = data_name[0] + " " + data_name[1][0] + "." + data_name[2][0] + "."
        buttons.append([
            InlineKeyboardButton(text=name, callback_data=f"coaches_show_{coach[0]}")
        ])

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def coach(c_id: int):
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🗑", callback_data=f"coaches_delete_{c_id}"),
            InlineKeyboardButton(text="📝", callback_data=f"coaches_edit_{c_id}")
        ],
        [
            InlineKeyboardButton(text="Назад 🔙", callback_data=f"coaches_back_{c_id}"),
        ]
    ])


def coaches_del_proof(c_id: int):
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="❌", callback_data=f"coaches_del-no_{c_id}"),
            InlineKeyboardButton(text="✅", callback_data=f"coaches_del-yes_{c_id}")
        ]
    ])


async def exercises_page(page: int = 1):
    buttons = []
    page_list = await rq.get_exercises_page(page)

    for number in range(1, len(page_list) + 1):
        buttons.append([
            InlineKeyboardButton(text=page_list[number - 1][0], callback_data=f"exercises_show_{page}_{number}")
        ])

    count = await rq.cnt_exercises()

    if count > 5:
        buttons.append([])

        if not page == 1:
            buttons[-1].append(InlineKeyboardButton(text="⬅", callback_data="exercises_left_" + str(page)))

        if not page == (count + 4) // 5:
            buttons[-1].append(InlineKeyboardButton(text="➡", callback_data="exercises_right_" + str(page)))

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def exercises(page: int, number: int):
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🗑", callback_data=f"exercises_delete_{page}_{number}"),
        ],
        [
            InlineKeyboardButton(text="Назад 🔙", callback_data=f"exercises_back_{page}_{number}"),
        ]
    ])


def exercises_del_proof(page: int, number: int):
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="❌", callback_data=f"exercises_del-no_{page}_{number}"),
            InlineKeyboardButton(text="✅", callback_data=f"exercises_del-yes_{page}_{number}")
        ]
    ])


async def workouts_exercises_page(page: int = 1):
    buttons = []
    page_list = await rq.get_workouts_exercises(page)

    for number in range(1, len(page_list) + 1):
        exercise = page_list[number - 1]
        buttons.append([
            InlineKeyboardButton(text=exercise[1], callback_data=f"workouts_exercises_{exercise[0]}")
        ])

    count = await rq.cnt_exercises()

    if count > 5:
        buttons.append([])

        if not page == 1:
            buttons[-1].append(InlineKeyboardButton(text="⬅", callback_data="workouts_exercises_left_" + str(page)))

        if not page == (count + 4) // 5:
            buttons[-1].append(InlineKeyboardButton(text="➡", callback_data="workouts_exercises_right_" + str(page)))

    return InlineKeyboardMarkup(inline_keyboard=buttons)


async def workouts(number: int, group_id: int):
    buttons = []
    count = await rq.cnt_workouts(group_id)

    if not count == 1:
        if not number == 1:
            buttons.append(InlineKeyboardButton(text="⬅", callback_data=f"workouts_left_{group_id}_{number}"))
        if not number == count:
            buttons.append(InlineKeyboardButton(text="➡", callback_data=f"workouts_right_{group_id}_{number}"))

    kb = InlineKeyboardMarkup(inline_keyboard=[
        buttons,
        [
            InlineKeyboardButton(text="🗑", callback_data=f"workouts_delete_{group_id}_{number}")
        ],
        [
            InlineKeyboardButton(text="Назад 🔙", callback_data=f"workouts_back_{group_id}_{number}")
        ]
    ])
    return kb


def workouts_del_proof(number: int, group_id: int):
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="❌", callback_data=f"workouts_del-no_{group_id}_{number}"),
            InlineKeyboardButton(text="✅", callback_data=f"workouts_del-yes_{group_id}_{number}")
        ]
    ])


def workouts_del_ready(group_id: int, number: int):
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Готово ✅", callback_data=f"workouts_ready_{group_id}_{number}")
        ]
    ])


async def admins_page():
    buttons = []
    admins_list = await rq.get_admins_page()

    for admin in admins_list:
        buttons.append([
            InlineKeyboardButton(text=admin[1], callback_data=f"admins_show_{admin[0]}")
        ])

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def admin(admin_id: int):
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🗑", callback_data=f"admins_delete_{admin_id}"),
        ],
        [
            InlineKeyboardButton(text="Назад 🔙", callback_data=f"admins_back_0"),
        ]
    ])


def admins_del_proof(admin_id: int):
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="❌", callback_data=f"admins_del-no_{admin_id}"),
            InlineKeyboardButton(text="✅", callback_data=f"admins_del-yes_{admin_id}")
        ]
    ])


def schedule_category(mode: str):
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Группы", callback_data=f"schedule_{mode}_groups")
        ],
        [
            InlineKeyboardButton(text="Тренеры", callback_data=f"schedule_{mode}_coaches")
        ]
    ])


async def schedule_groups_page(mode: str):
    buttons = []
    groups_list = await rq.get_groups_page()

    for group in groups_list:
        buttons.append([
            InlineKeyboardButton(text=group[1], callback_data=f"schedule_{mode}_groups_{group[0]}")
        ])

    buttons.append([
        InlineKeyboardButton(text="Назад 🔙", callback_data=f"schedule_{mode}_groups_back")
    ])

    return InlineKeyboardMarkup(inline_keyboard=buttons)


async def schedule_coaches_page(mode: str):
    buttons = []
    coaches_list = await rq.get_coaches_page()

    for coach in coaches_list:
        data_name = coach[1].split()
        name = data_name[0] + " " + data_name[1][0] + "." + data_name[2][0] + "."
        buttons.append([
            InlineKeyboardButton(text=name, callback_data=f"schedule_{mode}_coaches_{coach[0]}")
        ])

    buttons.append([
        InlineKeyboardButton(text="Назад 🔙", callback_data=f"schedule_{mode}_coaches_back")
    ])

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def schedule_weekdays(mode: str, category: str, target: str):
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Понедельник", callback_data=f"schedule_{mode}_{category}_{target}_monday")
        ],
        [
            InlineKeyboardButton(text="Вторник", callback_data=f"schedule_{mode}_{category}_{target}_tuesday")
        ],
        [
            InlineKeyboardButton(text="Среда", callback_data=f"schedule_{mode}_{category}_{target}_wednesday")
        ],
        [
            InlineKeyboardButton(text="Четверг", callback_data=f"schedule_{mode}_{category}_{target}_thursday")
        ],
        [
            InlineKeyboardButton(text="Пятница", callback_data=f"schedule_{mode}_{category}_{target}_friday")
        ],
        [
            InlineKeyboardButton(text="Суббота", callback_data=f"schedule_{mode}_{category}_{target}_saturday")
        ],
        [
            InlineKeyboardButton(text="Воскресенье", callback_data=f"schedule_{mode}_{category}_{target}_sunday")
        ],
        [
            InlineKeyboardButton(text="Назад 🔙", callback_data=f"schedule_{mode}_{category}_{target}_back")
        ]
    ])


def schedule_dates(mode: str, category: str, target: str, dates: list):
    weekdays = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]
    buttons = []

    for i in range(7):
        day = dates[i].strftime("%d.%m.%Y")
        text = day + " (" + weekdays[i] + ")"
        buttons.append([
            InlineKeyboardButton(text=text, callback_data=f"schedule_{mode}_{category}_{target}_{day}")
        ])

    control = []
    if date.today().isocalendar()[1] - dates[0].isocalendar()[1] < 4:
        control.append(InlineKeyboardButton(
            text="⬅", callback_data=f"schedule_{mode}_{category}_{target}_left-{dates[0].strftime("%d.%m.%Y")}")
        )

    if dates[6].isocalendar()[1] - date.today().isocalendar()[1] < 8:
        control.append(InlineKeyboardButton(
            text="➡", callback_data=f"schedule_{mode}_{category}_{target}_right-{dates[6].strftime("%d.%m.%Y")}")
        )

    buttons.append(control)
    buttons.append([
        InlineKeyboardButton(text="Назад 🔙", callback_data=f"schedule_{mode}_{category}_{target}_back")
    ])

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def schedule_day(mode: str, category: str, target: str, day: str):
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="➕", callback_data=f"schedule_{mode}_{category}_{target}_{day}_add"),
            InlineKeyboardButton(text="🗑", callback_data=f"schedule_{mode}_{category}_{target}_{day}_delete"),
            InlineKeyboardButton(text="📝", callback_data=f"schedule_{mode}_{category}_{target}_{day}_edit")
        ],
        [
            InlineKeyboardButton(text="Назад 🔙", callback_data=f"schedule_{mode}_{category}_{target}_{day}_back")
        ]
    ])
