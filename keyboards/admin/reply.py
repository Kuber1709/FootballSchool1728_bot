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
    ],
    [
        KeyboardButton(text="Настройки ⚙")
    ]
], resize_keyboard=True, input_field_placeholder="Выберите пункт меню")

advertisements = ReplyKeyboardMarkup(keyboard=[
    [
      KeyboardButton(text="Создать объявление 📢")
    ],
    [
        KeyboardButton(text="Назад 🔙")
    ]
], resize_keyboard=True)

undo = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text="Отмена 🚫")
    ]
], resize_keyboard=True)