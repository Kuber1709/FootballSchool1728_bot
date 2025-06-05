from aiogram import Router

from middlewares import RegistrationMiddleware, DeleteMenuMiddleware, DeleteMessageMiddleware
from .admin_router import admin_router
from .user_router import user_router

router = Router()
router.message.outer_middleware.register(RegistrationMiddleware())
router.message.outer_middleware.register(DeleteMessageMiddleware())
router.message.middleware.register(DeleteMenuMiddleware())
router.include_router(user_router)
router.include_router(admin_router)
