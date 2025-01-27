from src.handlers.crud.courses.interface import (
    CourseInterfaceAdmin,
    UpdateTitle,
    UpdateMedia,
    UpdateDescription,
    AddCourse
)
from src.handlers.crud.courses import UpdatePrice
from src.handlers.admin.keyboard import ADMIN_KEYBOARD
from aiogram.types import Message, CallbackQuery
from aiogram.filters.state import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram import Router, F


router = Router()
course_interface = CourseInterfaceAdmin()


@router.message(StateFilter(None), Command("Добавить курс"))
@router.message(StateFilter(None), F.text == "Добавить курс")
async def start_add_new_course_handler(message: Message, state: FSMContext):
    await course_interface.start_add_new_course(message=message, state=state)


@router.message(StateFilter("*"), Command("отмена"))
@router.message(StateFilter("*"), F.text == "отмена")
async def cancel_handler(message: Message, state: FSMContext):
    await course_interface.cancel(message=message, state=state, keyboard=ADMIN_KEYBOARD)


@router.message(StateFilter("*"), Command("назад"))
@router.message(StateFilter("*"), F.text == "назад")
async def cancel_handler(message: Message, state: FSMContext):
    await course_interface.previous(message=message, state=state)


@router.message(AddCourse.title, F.text)
async def add_new_title_handler(message: Message, state: FSMContext):
    await course_interface.add_title(message=message, state=state)


@router.message(AddCourse.description, F.text)
async def add_new_description_handler(message: Message, state: FSMContext):
    await course_interface.add_description(message=message, state=state)


@router.message(AddCourse.media_url, F.photo)
async def add_new_media_handler(message: Message, state: FSMContext):
    await course_interface.add_media(message=message, state=state)

@router.message(AddCourse.price, F.text)
async def add_price(message: Message, state: FSMContext):
    await course_interface.add_price(message=message, state=state, keyboard=ADMIN_KEYBOARD)


@router.message(Command("Получить список курсов"))
@router.message(F.text == "Получить список курсов")
async def get_courses_list_handler(message: Message):
    await course_interface.send_all_courses(message=message)


@router.callback_query(F.data.startswith("delete_"))
async def delete_course_handler(callback_query: CallbackQuery):
    await course_interface.delete_course_callback(
        callback_query=callback_query,
        keyboard=ADMIN_KEYBOARD
    )


@router.callback_query(StateFilter(None), F.data.startswith("title_"))
async def edit_title_callback(callback_query: CallbackQuery, state: FSMContext):
    await course_interface.update_title_callback(callback_query=callback_query, state=state)


@router.message(UpdateTitle.title, F.text)
async def edit_title(message: Message, state: FSMContext):
    await course_interface.update_title(state=state, message=message, keyboard=ADMIN_KEYBOARD)


@router.callback_query(StateFilter(None), F.data.startswith("description_"))
async def edit_description_callback(callback_query: CallbackQuery, state: FSMContext):
    await course_interface.update_description_callback(callback_query=callback_query, state=state)


@router.message(UpdateDescription.description, F.text)
async def edit_description(message: Message, state: FSMContext):
    await course_interface.update_description(state=state, message=message, keyboard=ADMIN_KEYBOARD)


@router.callback_query(StateFilter(None), F.data.startswith("media_"))
async def edit_media_callback(callback_query: CallbackQuery, state: FSMContext):
    await course_interface.update_media_callback(callback_query=callback_query, state=state)

@router.message(UpdateMedia.media_url, F.photo)
async def edit_media(message: Message, state: FSMContext):
    await course_interface.update_media(state=state, message=message, keyboard=ADMIN_KEYBOARD)


@router.callback_query(StateFilter(None), F.data.startswith("price_"))
async def edit_price_callback(callback_query: CallbackQuery, state: FSMContext):
    await course_interface.update_price_callback(callback_query=callback_query, state=state)

@router.message(UpdatePrice.price, F.text)
async def edit_price(message: Message, state: FSMContext):
    await course_interface.update_price(state=state, message=message, keyboard=ADMIN_KEYBOARD)
