from aiogram import Router

from .start import admin_router as start_router
from .files import admin_router as files_router
from .link import admin_router as link_router
from .edit import admin_router as edit_router
from .socials import admin_router as social_router
from .filter import admin_filter

admin_router = Router()
admin_router.message.filter(admin_filter)

admin_router.include_router(start_router)
admin_router.include_router(files_router)
admin_router.include_router(link_router)
admin_router.include_router(edit_router)
admin_router.include_router(social_router)
