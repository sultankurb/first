from src.handlers.crud.courses.interface import CourseInterfaceAdmin
from src.filter.filter import ChatTypeFilter, IsAdmin
from .events import router as events
from .keyboard import ADMIN_KEYBOARD
from .course import router as course
from aiogram.filters import Command
from aiogram.types import Message
from aiogram import Router


admin = Router()
admin.include_router(course)
admin.include_router(events)
admin.message.filter(ChatTypeFilter(chat_types=["private"]), IsAdmin())
course_interface = CourseInterfaceAdmin()


@admin.message(Command("admin"))
async def admin_cms(message: Message):
    await message.answer(text="Что бы вы хотели сделать", reply_markup=ADMIN_KEYBOARD)
