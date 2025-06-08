from aiogram import Router

from middlewares import (RegistrationMiddleware, DeleteMenuMiddleware, DeleteMessageMiddleware, SyncFSMMiddleware,
                         QueueMiddleware, ClearStateMiddleware)
from .admin_router import admin_router
from .user_router import user_router

router = Router()

router.message.outer_middleware.register(QueueMiddleware())
router.callback_query.outer_middleware.register(QueueMiddleware())

router.message.outer_middleware.register(SyncFSMMiddleware())
router.callback_query.outer_middleware.register(SyncFSMMiddleware())

router.message.outer_middleware.register(RegistrationMiddleware())
router.callback_query.outer_middleware.register(RegistrationMiddleware())

router.message.outer_middleware.register(DeleteMessageMiddleware())
router.callback_query.outer_middleware.register(DeleteMessageMiddleware())

router.message.middleware.register(DeleteMenuMiddleware())
router.callback_query.middleware.register(DeleteMenuMiddleware())

router.message.middleware.register(ClearStateMiddleware())

router.include_router(user_router)
router.include_router(admin_router)
