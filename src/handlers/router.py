from .admin.router import admin
from .users.router import users
from aiogram import Router

router = Router()
router.include_router(router=admin)
router.include_router(router=users)
