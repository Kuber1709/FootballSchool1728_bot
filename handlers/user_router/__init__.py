from aiogram import Router

from filters import IsUserFilter
from .callback import user_callback_router
from .messages import user_messages_router

user_router = Router()
user_router.message.filter(IsUserFilter())
user_router.callback_query.filter(IsUserFilter())
user_router.include_router(user_messages_router)
user_router.include_router(user_callback_router)
