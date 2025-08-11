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
    ]
], resize_keyboard=True, input_field_placeholder="Выберите пункт меню")
