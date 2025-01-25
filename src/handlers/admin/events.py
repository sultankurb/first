from src.handlers.crud.events import (
    EventsInterface,
    AddEvent,
    UpdateTitle,
    UpdateDescription,
    UpdateMedia,
    UpdateActive
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
