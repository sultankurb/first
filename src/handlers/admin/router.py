from src.handlers.crud.courses import CourseInterfaceAdmin, AddCourse, UpdateCourse
from .keyboard import ADMIN_KEYBOARD, UPDATE_KEYBOARD
from src.filter.filter import ChatTypeFilter, IsAdmin
from aiogram.filters import Command, StateFilter
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram import Router, F


admin = Router()
admin.message.filter(ChatTypeFilter(chat_types=["private"]), IsAdmin())
course_interface = CourseInterfaceAdmin()

@admin.message(Command("admin"))
async def admin_cms(message: Message):
    await message.answer(text="Что бы вы хотели сделать", reply_markup=ADMIN_KEYBOARD)


@admin.message(Command("Получить список курсов"))
@admin.message(F.text == "Получить список курсов")
async def get_courses_list_handler(message: Message):
    await course_interface.send_all_courses(message=message)


@admin.callback_query(F.data.startswith("delete_"))
async def delete_course_handler(callback_query: CallbackQuery):
    await course_interface.delete_course_callback(
        callback_query=callback_query,
        keyboard=ADMIN_KEYBOARD
    )

#
# @admin.callback_query(StateFilter(None), F.data.startswith("update_"))
# async def update_handler(callback_query: CallbackQuery):
#     await course_interface.update_callback(callback_query=callback_query, keyboard=UPDATE_KEYBOARD)


# @admin.message(StateFilter(None),Command("обновить название курса"))
# async def start_update_course_title(message: Message, state: FSMContext):
#     await course_interface.start_update_title(message, state)
#
#
# @admin.message(UpdateCourse.title, F.text)
# async def update_course_title_handler(message: Message, state: FSMContext):
#     await course_interface.update_title(message, state)


# @admin.message(StateFilter(None),Command("обновить описание"))
# async def start_update_course_description(message: Message, state: FSMContext):
#     await course_interface.start_update_description(message, state)
#
#
# @admin.message(UpdateCourse.description, F.text)
# async def update_course_description_handler(message: Message, state: FSMContext):
#     await course_interface.update_description(message, state)
#
#
# @admin.message(StateFilter(None),Command("Обновить фото"))
# async def start_update_course_media(message: Message, state: FSMContext):
#     await course_interface.start_update_media(message, state)
#
# @admin.message(UpdateCourse.media_url, F.photo)
# async def update_course_media_handler(message: Message, state: FSMContext):
#     await course_interface.update_media(message, state)


@admin.message(StateFilter(None), Command("Добавить курс"))
@admin.message(StateFilter(None), F.text == "Добавить курс")
async def start_add_new_course_handler(message: Message, state: FSMContext):
    await course_interface.start_add_new_course(message=message, state=state)


@admin.message(AddCourse.title, F.text)
async def add_new_title_handler(message: Message, state: FSMContext):
    await course_interface.add_title(message=message, state=state)


@admin.message(AddCourse.description, F.text)
async def add_new_description_handler(message: Message, state: FSMContext):
    await course_interface.add_description(message=message, state=state)


@admin.message(AddCourse.media_url, F.photo)
async def add_new_media_handler(message: Message, state: FSMContext):
    await course_interface.add_media(message=message, state=state, keyboard=ADMIN_KEYBOARD)
