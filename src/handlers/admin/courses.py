from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from src.database.crud.courses import CoursesRepository
from src.keyboards.in_line import get_callback_buttons
from aiogram.filters import Command, StateFilter
from src.keyboards.keyboard import get_keyboard
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram import Router, F


courses = Router()
ADMIN_KB = get_keyboard(
    "Добавить новый курс",
    "Курсы",
    "Добавить новое событие",
    "События",
)
repo = CoursesRepository()


class AddCourses(StatesGroup):
    title = State()
    description = State()
    images_url = State()
    texts = {
        "AddCourses:title": "Введите название заново:",
        "AddCourses:description": "Введите описание заново:",
        "AddCourses:image_url": "Этот стейт последний, поэтому...",
    }
    course_for_change = None


@courses.message(Command("admin"))
async def admin_router(message: Message):
    await message.answer(text="Что бы вы хоте сделать?", reply_markup=ADMIN_KB)


@courses.message(StateFilter(None), Command("Добавить новый курс"))
@courses.message(StateFilter(None), F.text == "Добавить новый курс")
async def craete_course(message: Message, state: FSMContext):
    await message.answer(
        text="Вы выбрали добавить курс\nВведите название курса",
        reply_markup=ReplyKeyboardRemove(),
    )
    await state.set_state(AddCourses.title)


@courses.message(StateFilter("*"), Command("отмена"))
@courses.message(StateFilter("*"), F.text.casefold() == "отмена")
async def cancel(message: Message, state: FSMContext):
    current_states = await state.get_state()
    if current_states is None:
        return
    await state.clear()
    await message.answer(text="Действие отменино", reply_markup=ADMIN_KB)


@courses.message(Command("назад"))
@courses.message(F.text.casefold() == "назад")
async def cancel_handler(message: Message, state: FSMContext):
    current_state = await state.get_state()

    if current_state == AddCourses.title:
        await message.answer(
            'Предидущего шага нет, или введите название курса или напишите "отмена"'
        )
        return

    previous = None
    for step in AddCourses.__all_states__:
        if step.state == current_state:
            await state.set_state(previous)
            await message.answer(
                f"Ок, вы вернулись к прошлому шагу \n {AddCourses.texts[previous.state]}"
            )
            return
        previous = step


@courses.message(AddCourses.title, F.text)
async def create_title(message: Message, state: FSMContext):
    await state.update_data(title=message.text)
    await message.answer(text="Введите описание")
    await state.set_state(AddCourses.description)


@courses.message(AddCourses.description, F.text)
async def create_description(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await message.answer(text="Отправте фото для курса")
    await state.set_state(AddCourses.images_url)


@courses.message(AddCourses.images_url, F.photo)
async def create_photo(message: Message, state: FSMContext):
    await state.update_data(images_url=message.photo[-1].file_id)
    await message.answer(text="Курс успешно добавлен", reply_markup=ADMIN_KB)
    data = await state.get_data()
    await repo.insert_data(data=data)
    await state.clear()


@courses.message(Command("Курсы"))
@courses.message(F.text == "Курсы")
async def get_courses(message: Message):
    courses_list = await repo.select_all()
    if courses_list:
        for course in courses_list:
            await message.answer_photo(
                photo=course.images_url,
                caption=f"{course.title}\n{course.description}",
                reply_markup=get_callback_buttons(
                    btns={
                        "Удалить": f"delete_{course.pk}",
                    },
                ),
            )
    else:
        await message.answer(text="Здесь пока ничего нету")


@courses.callback_query(F.data.startswith("delete_"))
async def delete_course(callback_query: CallbackQuery):
    course_id = callback_query.data.split("_")[-1]
    await repo.delete_data(pk=int(course_id))
    await callback_query.answer(text="Курс Удалён", show_alert=True)
    await callback_query.message.answer(text="Курс Удалён", reply_markup=ADMIN_KB)
