from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from src.keyboards.in_line import get_callback_buttons
from src.settings import async_session_maker
from src.utils import AdminInterface, UsersInterface
from aiogram.fsm.context import FSMContext
from src.database.models import Event
from .send_events import send_event
from sqlalchemy import select
from .states import (
    AddEvent,
    UpdateMediaEvent,
    UpdateTitleEvent,
    UpdateActiveEvent,
    UpdateDescriptionEvent,
)


class EventsInterface(AdminInterface):
    model = Event

    async def send_events(self, message: Message):
        events = await self.get_all()
        if events:
            for i in events:
                await message.answer_photo(
                    photo=i.media_url,
                    caption=f"{i.title}\n{i.description}\n{i.is_active}",
                    reply_markup=get_callback_buttons(
                        btns={
                            "заглавие": f"eventtitle_{i.pk}",
                            "описание": f"eventdescription_{i.pk}",
                            "фото": f"eventphoto_{i.pk}",
                            "статус": f"eventstatus_{i.is_active}",
                            "удалить": f"eventdelete_{i.pk}"
                        }
                    )
                )
        else:
            await message.answer(text='здесь ничего нет пока что')

    async def delete_callback(self, callback_query: CallbackQuery):
        pk = callback_query.data.split("_")[-1]
        await self.delete_one(pk=int(pk))
        await callback_query.message.answer(text="событие было удалено")

    @classmethod
    async def start_create(cls, message: Message, state: FSMContext):
        await message.answer(text='пришлите мне новое название', reply_markup=ReplyKeyboardRemove())
        await state.set_state(AddEvent.title)

    @classmethod
    async def add_title(cls, message: Message, state: FSMContext):
        await state.update_data(title=message.text)
        await message.answer(text='А теперь пришлите мне описание')
        await state.set_state(AddEvent.description)

    @classmethod
    async def add_description(cls, message: Message, state: FSMContext):
        await state.update_data(description=message.text)
        await message.answer(text='Хорошо, отправьте мне изображение')
        await state.set_state(AddEvent.media_url)

    @classmethod
    async def add_media(cls, message: Message, state: FSMContext):
        await state.update_data(media_url=message.photo[-1].file_id)
        await message.answer(text='Окей, пришлите мне статус')
        await state.set_state(AddEvent.is_active)

    async def add_status(
            self,
            message: Message,
            state: FSMContext,
            keyboard
    ):
        if message == "активный":
            await state.update_data(is_active=True)
        elif message == "неактивный":
            await state.update_data(is_active=False)
        data = await state.get_data()
        await message.answer(text="событие было добавлено", reply_markup=keyboard)
        await send_event(new_data=data)
        await self.add_one(data=data)
        await state.clear()

    async def update_title_callback(self, callback_query: CallbackQuery, state: FSMContext):
        event = await self.get_one(pk=int(callback_query.data.split("_")[-1]))
        UpdateTitleEvent.for_update = event
        await state.set_state(UpdateTitleEvent.title_event)
        await callback_query.message.answer(text='Пришлите, пожалуйста, новое название', reply_markup=ReplyKeyboardRemove())

    async def update_title(self, message: Message, state: FSMContext, keyboard):
        await state.update_data(title=message.text)
        data = await state.get_data()
        await self.edit_one(pk=UpdateTitleEvent.for_update.pk, data=data)
        await message.answer(text='название было обновлено', reply_markup=keyboard)
        UpdateTitleEvent.for_update = None
        await state.clear()

    async def update_description_callback(self, callback_query: CallbackQuery, state: FSMContext):
        event = await self.get_one(pk=int(callback_query.data.split("_")[-1]))
        UpdateDescriptionEvent.for_update = event
        await state.set_state(UpdateDescriptionEvent.description_event)
        await callback_query.message.answer(text='Пришлите, пожалуйста, новое описание', reply_markup=ReplyKeyboardRemove())

    async def update_description(self, message: Message, state: FSMContext, keyboard):
        await state.update_data(description=message.text)
        data = await state.get_data()
        await self.edit_one(pk=UpdateDescriptionEvent.for_update.pk, data=data)
        await message.answer(text="описание было обновлено", reply_markup=keyboard)
        UpdateDescriptionEvent.for_update = None
        await state.clear()

    async def update_media_callback(self, callback_query: CallbackQuery, state: FSMContext):
        event = await self.get_one(pk=int(callback_query.data.split("_")[-1]))
        UpdateMediaEvent.for_update = event
        await state.set_state(UpdateMediaEvent.media_url_event)
        await callback_query.message.answer(text='пришлите, пожалуйста, новую фотографию', reply_markup=ReplyKeyboardRemove())

    async def update_media(self, message: Message, state: FSMContext, keyboard):
        await state.update_data(media_url=message.photo[-1].file_id)
        data = await state.get_data()
        await self.edit_one(pk=UpdateMediaEvent.for_update.pk, data=data)
        await message.answer(text="фотография была обновлена", reply_markup=keyboard)
        UpdateMediaEvent.for_update = None
        await state.clear()

    async def update_status_callback(self, callback_query: CallbackQuery, state: FSMContext):
        pk = callback_query.data.split("_")[-1]
        event = await self.get_one(pk=int(callback_query.data.split("_")[-1]))
        UpdateActiveEvent.for_update = event
        await state.set_state(UpdateActiveEvent.active_event)
        await callback_query.message.answer(text='Пришлите мне новый статус', reply_markup=ReplyKeyboardRemove())

    async def update_status(self, message: Message, state: FSMContext, keyboard):
        await state.update_data(media_url=message.photo[-1].file_id)
        data = await state.get_data()
        await self.edit_one(pk=UpdateActiveEvent.for_update.pk, data=data)
        await message.answer(text='Статус был обновлен', reply_markup=keyboard)
        UpdateActiveEvent.for_update = None
        await state.clear()

    @classmethod
    async def cancel(cls, message: Message, state: FSMContext, keyboard):
        current_states = await state.get_state()
        if current_states is None:
            return
        await state.clear()
        await message.answer(text="Действие отменено", reply_markup=keyboard)

    @classmethod
    async def previous(cls, message: Message, state: FSMContext):
        current_state = await state.get_state()

        if current_state == AddEvent.title:
            await message.answer(
                "Предыдущего шага нет, или отправьте сообщение 'отмена'!"
            )
            return

        previous = None
        for step in AddEvent.__all_states__:
            if step.state == current_state:
                await state.set_state(previous)
                await message.answer(
                    f"Хорошо, вы  вернулсь к предыдущему шагу\n {AddEvent.texts[previous.state]}"
                )
                return
            previous = step


class UsersEventsInterface(UsersInterface):
    model = Event

    async def __select_filtered(self):
        async with async_session_maker() as session:
            stmt = select(self.model).filter_by(is_active=True)
            result = await session.execute(stmt)
            return result.scalars().all()

    async def send_all(self, message: Message):
        events_list = await self.__select_filtered()
        if events_list:
            for event in events_list:
                await message.answer_photo(
                    photo=event.media_url,
                    caption=f"{event.title}\n\n{event.description}"
                )
        else:
            await message.answer(text='нет никаких событий')
