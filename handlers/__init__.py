from aiogram import Router

from middlewares.registration import RegistrationMiddleware
from .admin_router import admin_router
from .user_router import user_router

router = Router()
router.message.outer_middleware(RegistrationMiddleware())
router.include_router(user_router)
router.include_router(admin_router)
