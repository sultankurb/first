from src.filters.chat_types import ChatTypeFilter, IsAdmin
from .events import event
from .courses import courses
from aiogram import Router


admin = Router()
admin.message.filter(ChatTypeFilter(chat_types=["private"]), IsAdmin())
admin.include_router(router=courses)
admin.include_router(router=event)
