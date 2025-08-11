from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

undo = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text="Отмена 🚫")
    ]
], resize_keyboard=True)
