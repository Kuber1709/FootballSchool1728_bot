from aiogram import Router

from filters import IsAdminFilter
from .callback import admin_callback_router
from .messages import admin_messages_router

admin_router = Router()
admin_router.message.filter(IsAdminFilter())
admin_router.callback_query.filter(IsAdminFilter())
admin_router.include_router(admin_messages_router)
admin_router.include_router(admin_callback_router)
