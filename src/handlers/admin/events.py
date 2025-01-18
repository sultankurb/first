from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from src.keyboards.in_line import get_callback_buttons
from src.database.crud.events import EventsRepository
from aiogram.filters import Command, StateFilter
from src.keyboards.keyboard import get_keyboard
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram import Router, F


event = Router()
ADMIN_KB = get_keyboard(
    "Добавить новый курс",
    "Курсы",
    "Добавить новое событие",
    "События",
)
repo_event = EventsRepository()


class AddEvents(StatesGroup):
    title = State()
    description = State()
    media_url = State()
    texts = {
        "AddCourses:title": "Введите название заново:",
        "AddCourses:description": "Введите описание заново:",
        "AddCourses:media_url": "Этот стейт последний, поэтому...",
    }
    event_for_change = None


@event.message(Command("admin"))
async def admin_router(message: Message):
    await message.answer(text="Что бы вы хоте сделать?", reply_markup=ADMIN_KB)


@event.message(StateFilter(None), Command("Добавить новое событие"))
@event.message(StateFilter(None), F.text == "Добавить новое событие")
async def add_event(message: Message, state: FSMContext):
    await message.answer(
        text="Вы выбрали добавить событие\nВведите название события",
        reply_markup=ReplyKeyboardRemove(),
    )
    await state.set_state(AddEvents.title)


@event.message(StateFilter("*"), Command("отмена"))
@event.message(StateFilter("*"), F.text.casefold() == "отмена")
async def cancel_event(message: Message, state: FSMContext):
    current_states = await state.get_state()
    if current_states is None:
        return
    await state.clear()
    await message.answer(text="Действие отменино", reply_markup=ADMIN_KB)


@event.message(Command("назад"))
@event.message(F.text.casefold() == "назад")
async def cancel_handler_event(message: Message, state: FSMContext):
    current_state = await state.get_state()

    if current_state == AddEvents.title:
        await message.answer(
            'Предидущего шага нет, или введите название курса или напишите "отмена"'
        )
        return

    previous = None
    for step in AddEvents.__all_states__:
        if step.state == current_state:
            await state.set_state(previous)
            await message.answer(
                f"Ок, вы вернулись к прошлому шагу \n {AddEvents.texts[previous.state]}"
            )
            return
        previous = step


@event.message(AddEvents.title, F.text)
async def add_title_event(message: Message, state: FSMContext):
    await state.update_data(title=message.text)
    await message.answer(text="Введите описание")
    await state.set_state(AddEvents.description)


@event.message(AddEvents.description, F.text)
async def add_description_event(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await message.answer(text="Отправте фото для события")
    await state.set_state(AddEvents.media_url)


@event.message(AddEvents.media_url, F.photo)
async def add_photo_event(message: Message, state: FSMContext):
    await state.update_data(media_url=message.photo[-1].file_id)
    await message.answer(text="Событие успешно добавлен", reply_markup=ADMIN_KB)
    data = await state.get_data()
    await repo_event.insert_data(data=data)
    await state.clear()


@event.message(Command("События"))
@event.message(F.text == "События")
async def get_events(message: Message):
    events_list = await repo_event.filtered_search()
    if events_list:
        for event_media in events_list:
            await message.answer_photo(
                photo=event_media.media_url,
                caption=f"{event_media.title}\n{event_media.description}",
                reply_markup=get_callback_buttons(
                    btns={
                        "Удалить": f"delete_{event_media.pk}",
                    },
                ),
            )
    else:
        await message.answer(text="Здесь пока ничего нету")


@event.callback_query(F.data.startswith("delete_"))
async def delete_event(callback_query: CallbackQuery):
    event_id = callback_query.data.split("_")[-1]
    await repo_event.delete_data(pk=int(event_id))
    await callback_query.answer(text="Событие Удалённо", show_alert=True)
    await callback_query.message.answer(text="Событие Удалённо", reply_markup=ADMIN_KB)
