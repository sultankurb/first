from aiogram.fsm.state import State, StatesGroup


class AddCourse(StatesGroup):
    title = State()
    description = State()
    media_url = State()
    price = State()
    texts = {
        "AddCourse:title": "Пришлете мне название нового курса:",
        "AddCourse:description": "А теперь пришлите мне описание этого курса:",
        "AddCourse:image_url": "пришлите мне, пожалуйста, новое изображение:",
        "AddCourse:price": "пришлите мне, пожалуйста, новую цену:"
    }


class UpdateTitleCourses(StatesGroup):
    title_courses = State()

    for_update = None

class UpdateDescriptionCourses(StatesGroup):
    description_Courses = State()

    for_update = None

class UpdateMediaCourses(StatesGroup):
    media_url_courses = State()

    for_update = None


class UpdatePriceCourses(StatesGroup):
    price_courses = State()

    for_update = None
