from aiogram.fsm.state import StatesGroup, State


class AddEvent(StatesGroup):
    title = State()
    description = State()
    media_url = State()
    is_active = State()

    texts = {
        "AddCourse:title": "Пришлете мне название нового курса:",
        "AddCourse:description": "А теперь пришлите мне описание этого курса:",
        "AddCourse:image_url": "пришлите мне, пожалуйста, новое изображение:",
        "AddCourse:price": "пришлите мне, пожалуйста, новую цену:"
    }


class UpdateTitleEvent(StatesGroup):
    title_event = State()

    for_update = None


class UpdateDescriptionEvent(StatesGroup):
    description_event = State()

    for_update = None


class UpdateMediaEvent(StatesGroup):
    media_url_event = State()

    for_update = None


class UpdateActiveEvent(StatesGroup):
    active_event = State()

    for_update = None
