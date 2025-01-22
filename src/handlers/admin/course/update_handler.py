from src.handlers.crud.courses import CourseInterfaceAdmin, UpdateTitle, UpdateMedia, UpdateDescription
from src.handlers.admin.keyboard import ADMIN_KEYBOARD
from aiogram.types import Message, CallbackQuery
from aiogram.filters.state import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram import Router, F

router = Router()
interface = CourseInterfaceAdmin()

@router.message(Command("Получить список курсов"))
@router.message(F.text == "Получить список курсов")
async def get_courses_list_handler(message: Message):
    await interface.send_all_courses(message=message)


@router.callback_query(F.data.startswith("delete_"))
async def delete_course_handler(callback_query: CallbackQuery):
    await interface.delete_course_callback(
        callback_query=callback_query,
        keyboard=ADMIN_KEYBOARD
    )


@router.callback_query(StateFilter(None), F.data.startswith("title_"))
async def edit_title_callback(callback_query: CallbackQuery, state: FSMContext):
    await interface.update_title_callback(callback_query=callback_query, state=state)


@router.message(UpdateTitle.title, F.text)
async def edit_title(message: Message, state: FSMContext):
    await interface.update_title(state=state, message=message, keyboard=ADMIN_KEYBOARD)


@router.callback_query(StateFilter(None), F.data.startswith("description_"))
async def edit_description_callback(callback_query: CallbackQuery, state: FSMContext):
    await interface.update_description_callback(callback_query=callback_query, state=state)


@router.message(UpdateDescription.description, F.text)
async def edit_description(message: Message, state: FSMContext):
    await interface.update_description(state=state, message=message, keyboard=ADMIN_KEYBOARD)


@router.callback_query(StateFilter(None), F.data.startswith("media_"))
async def edit_media_callback(callback_query: CallbackQuery, state: FSMContext):
    await interface.update_media_callback(callback_query=callback_query, state=state)

@router.message(UpdateMedia.media_url, F.photo)
async def edit_media(message: Message, state: FSMContext):
    await interface.update_media(state=state, message=message, keyboard=ADMIN_KEYBOARD)
