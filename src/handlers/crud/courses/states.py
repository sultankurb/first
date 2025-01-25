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


class UpdateTitle(StatesGroup):
    title = State()

    for_update = None

class UpdateDescription(StatesGroup):
    description = State()

    for_update = None

class UpdateMedia(StatesGroup):
    media_url = State()

    for_update = None


class UpdatePrice(StatesGroup):
    price = State()

    for_update = None
