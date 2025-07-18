from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text="Объявления 📢"),
        KeyboardButton(text="Расписание 🔔")
    ],
    [
        KeyboardButton(text="Домашние тренировки 🏃")
    ],
    [
        KeyboardButton(text="Информация ℹ")
    ],
    [
        KeyboardButton(text="Админы 👨‍💻"),
        KeyboardButton(text="Группы 👥")
    ]
], resize_keyboard=True, input_field_placeholder="Выберите пункт меню")

undo = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text="Отмена 🚫")
    ]
], resize_keyboard=True)

advertisements_back = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text="Создать объявление 📢")
    ],
    [
        KeyboardButton(text="Назад 🔙")
    ]
], resize_keyboard=True)

information_back = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text="Добавить информацию ℹ")
    ],
    [
        KeyboardButton(text="Назад 🔙")
    ]
], resize_keyboard=True)

groups_back = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text="Добавить группу 👥")
    ],
    [
        KeyboardButton(text="Назад 🔙")
    ]
], resize_keyboard=True)

coaches_back = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text="Добавить тренера 👤")
    ],
    [
        KeyboardButton(text="Закрыть 🔙")
    ]
], resize_keyboard=True)

workouts_back = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text="Упражнения ⚽")
    ],
    [
        KeyboardButton(text="Добавить упражнение в тренировку 🏃")
    ],
    [
        KeyboardButton(text="Назад 🔙")
    ]
], resize_keyboard=True)

exercises_back = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text="Добавить упражнение ⚽")
    ],
    [
        KeyboardButton(text="Вернуться 🔙")
    ]
], resize_keyboard=True)

admins_back = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text="Добавить администратора 👨‍💻")
    ],
    [
        KeyboardButton(text="Назад 🔙")
    ]
], resize_keyboard=True)

schedule_back = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text="Тренеры 👤")
    ],
    [
        KeyboardButton(text="Изменить расписание 🔔")
    ],
    [
        KeyboardButton(text="Назад 🔙"),
    ]
], resize_keyboard=True)
