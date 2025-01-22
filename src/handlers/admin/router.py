from src.handlers.crud.courses import CourseInterfaceAdmin
from src.filter.filter import ChatTypeFilter, IsAdmin
from .course.main_router import router as course
from .keyboard import ADMIN_KEYBOARD
from aiogram.filters import Command
from aiogram.types import Message
from aiogram import Router, F


admin = Router()
admin.include_router(course)
admin.message.filter(ChatTypeFilter(chat_types=["private"]), IsAdmin())
course_interface = CourseInterfaceAdmin()

@admin.message(Command("admin"))
async def admin_cms(message: Message):
    await message.answer(text="Что бы вы хотели сделать", reply_markup=ADMIN_KEYBOARD)
