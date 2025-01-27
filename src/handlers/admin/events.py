from src.handlers.crud.events import (
    EventsInterface,
    AddEvent,
    UpdateTitleEvent,
    UpdateDescriptionEvent,
    UpdateMediaEvent,
    UpdateActiveEvent
)
from src.handlers.admin.keyboard import ADMIN_KEYBOARD
from aiogram.types import Message, CallbackQuery
from aiogram.filters.state import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram import Router, F


router = Router()
events_interface = EventsInterface()


@router.message(Command("Получить все события"))
@router.message(F.text == 'Получить все события')
async def get_all_events(message: Message):
    await events_interface.send_events(message=message)


@router.callback_query(F.data.startswith("eventdelete_"))
async def delete_course_handler(callback_query: CallbackQuery):
    await events_interface.delete_callback(
        callback_query=callback_query
    )


@router.callback_query(StateFilter(None), F.data.startswith("evnettitle_"))
async def edit_title_callback(callback_query: CallbackQuery, state: FSMContext):
    await events_interface.update_title_callback(callback_query=callback_query, state=state)


@router.message(UpdateTitleEvent.title_event, F.text)
async def edit_title(message: Message, state: FSMContext):
    await events_interface.update_title(state=state, message=message, keyboard=ADMIN_KEYBOARD)


@router.callback_query(StateFilter(None), F.data.startswith("evntdescription_"))
async def edit_description_callback(callback_query: CallbackQuery, state: FSMContext):
    await events_interface.update_description_callback(callback_query=callback_query, state=state)


@router.message(UpdateDescriptionEvent.description_event, F.text)
async def edit_description(message: Message, state: FSMContext):
    await events_interface.update_description(state=state, message=message, keyboard=ADMIN_KEYBOARD)


@router.callback_query(StateFilter(None), F.data.startswith("evnetphoto_"))
async def edit_media_callback(callback_query: CallbackQuery, state: FSMContext):
    await events_interface.update_media_callback(callback_query=callback_query, state=state)

@router.message(UpdateMediaEvent.media_url_event, F.photo)
async def edit_media(message: Message, state: FSMContext):
    await events_interface.update_media(state=state, message=message, keyboard=ADMIN_KEYBOARD)


@router.callback_query(StateFilter(None), F.data.startswith("evnetstatus_"))
async def edit_title_callback(callback_query: CallbackQuery, state: FSMContext):
    await events_interface.update_status_callback(callback_query=callback_query, state=state)


@router.message(UpdateActiveEvent.active_event, F.text)
async def edit_title(message: Message, state: FSMContext):
    await events_interface.update_status(state=state, message=message, keyboard=ADMIN_KEYBOARD)



@router.message(StateFilter(None), Command("Добавить новое событие"))
@router.message(StateFilter(None), F.text == "Добавить новое событие")
async def add_handler(message: Message, state: FSMContext):
    await events_interface.start_create(message=message, state=state)


@router.message(StateFilter("*"), Command("отмена"))
@router.message(StateFilter("*"), F.text == "отмена")
async def cancel_handler(message: Message, state: FSMContext):
    await events_interface.cancel(message=message, state=state, keyboard=ADMIN_KEYBOARD)


@router.message(StateFilter("*"), Command("назад"))
@router.message(StateFilter("*"), F.text == "назад")
async def cancel_handler(message: Message, state: FSMContext):
    await events_interface.previous(message=message, state=state)


@router.message(AddEvent.title, F.text)
async def add_new_title_handler(message: Message, state: FSMContext):
    await events_interface.add_title(message=message, state=state)


@router.message(AddEvent.description, F.text)
async def add_new_description_handler(message: Message, state: FSMContext):
    await events_interface.add_description(message=message, state=state)


@router.message(AddEvent.media_url, F.photo)
async def add_new_media_handler(message: Message, state: FSMContext):
    await events_interface.add_media(message=message, state=state)

@router.message(AddEvent.is_active, F.text)
async def add_new_price_handler(message: Message, state: FSMContext):
    await events_interface.add_status(message=message, state=state, keyboard=ADMIN_KEYBOARD)
