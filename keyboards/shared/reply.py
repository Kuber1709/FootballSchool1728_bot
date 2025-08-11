from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

undo = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text="Отмена 🚫")
    ]
], resize_keyboard=True)

back = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text="Назад 🔙")
    ]
], resize_keyboard=True)
