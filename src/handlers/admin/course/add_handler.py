from src.handlers.crud.courses import CourseInterfaceAdmin, AddCourse
from src.handlers.admin.keyboard import ADMIN_KEYBOARD
from aiogram.filters.state import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram.types import Message
from aiogram import Router, F


router = Router()
add_interface = CourseInterfaceAdmin()


@router.message(StateFilter(None), Command("Добавить курс"))
@router.message(StateFilter(None), F.text == "Добавить курс")
async def start_add_new_course_handler(message: Message, state: FSMContext):
    await add_interface.start_add_new_course(message=message, state=state)


@router.message(AddCourse.title, F.text)
async def add_new_title_handler(message: Message, state: FSMContext):
    await add_interface.add_title(message=message, state=state)


@router.message(AddCourse.description, F.text)
async def add_new_description_handler(message: Message, state: FSMContext):
    await add_interface.add_description(message=message, state=state)


@router.message(AddCourse.media_url, F.photo)
async def add_new_media_handler(message: Message, state: FSMContext):
    await add_interface.add_media(message=message, state=state, keyboard=ADMIN_KEYBOARD)
