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


def schedule_day(category: str, target: str, weekday: str, edit: bool):
    buttons = [
        InlineKeyboardButton(text="➕", callback_data=f"schedule_{category}_{target}_{weekday}_add")
    ]

    if edit:
        buttons.append(InlineKeyboardButton(text="📝", callback_data=f"schedule_{category}_{target}_{weekday}_edit"))

    return InlineKeyboardMarkup(inline_keyboard=[
        buttons,
        [
            InlineKeyboardButton(text="Назад 🔙", callback_data=f"schedule_{category}_{target}_{weekday}_back")
        ]
    ])


def schedule_lesson(category: str, target: str, weekday: str, mode: str, number: int, count: int):
    buttons = []
    cb_data = f"schedule_{category}_{target}_{weekday}_{mode}"

    if not count == 1:
        if not number == 1:
            buttons.append(InlineKeyboardButton(text="⬅", callback_data=f"{cb_data}_left-{number}"))
        if not number == count:
            buttons.append(InlineKeyboardButton(text="➡", callback_data=f"{cb_data}_right-{number}"))

    return InlineKeyboardMarkup(inline_keyboard=[
        buttons,
        [
            InlineKeyboardButton(text="🗑", callback_data=f"{cb_data}_delete-{number}")
        ],
        [
            InlineKeyboardButton(text="Назад 🔙", callback_data=f"{cb_data}_back")
        ]
    ])


def schedule_del_proof(category: str, target: str, weekday: str, mode: str, number: int):
    cb_data = f"schedule_{category}_{target}_{weekday}_{mode}"
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="❌", callback_data=f"{cb_data}_delNo_{number}"),
            InlineKeyboardButton(text="✅", callback_data=f"{cb_data}_delYes-{number}")
        ]
    ])


def schedule_add_proof(category: str, target: str, weekday: str, mode: str, target2: str, time: str):
    cb_data = f"schedule_{category}_{target}_{weekday}_{mode}_{target2}_{time}"
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="❌", callback_data=f"{cb_data}_add-no"),
            InlineKeyboardButton(text="✅", callback_data=f"{cb_data}_add-yes")
        ]
    ])
