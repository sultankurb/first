from aiogram import Router
from .add_handler import router as add
from .update_handler import router as update

router = Router()
router.include_router(update)
router.include_router(add)
