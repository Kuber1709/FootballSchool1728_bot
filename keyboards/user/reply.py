from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text="Объявления 📢"),
        KeyboardButton(text="Расписание 🔔")
    ],
    [
        KeyboardButton(text="Тренировки 🏃")
    ],
    [
        KeyboardButton(text="Информация ℹ")
    ]
], resize_keyboard=True, input_field_placeholder="Выберите пункт меню")

back = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text="Назад 🔙")
    ]
], resize_keyboard=True, input_field_placeholder="Выберите пункт меню")
