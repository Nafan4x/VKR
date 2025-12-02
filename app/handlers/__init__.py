from aiogram import Router

from .user_handlers import router as user_router
from .admin_handlers import admin_router
from .channel_hanlers import channel_router

router = Router()
router.include_router(admin_router)
router.include_router(user_router)
router.include_router(channel_router)
