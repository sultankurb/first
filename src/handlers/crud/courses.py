from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from src.keyboards.in_line import get_callback_buttons
from src.utils import AdminInterface, UsersInterface
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from src.database.models import Course


class AddCourse(StatesGroup):
    title = State()
    description = State()
    media_url = State()
    texts = {
        "AddTasks:title": "Пришлете мне название нового курса:",
        "AddTasks:description": "А теперь пришлите мне описание этого курса:",
        "AddTasks:image_url": "Это было последнее состояние...",
    }


class UpdateCourse(AddCourse):
    for_update = None


class CourseInterfaceAdmin(AdminInterface):
    model = Course

    async def send_all_courses(self, message: Message):
        course_list = await self.get_all()
        if course_list:
            for course in course_list:
                await message.answer_photo(
                    photo=course.media_url,
                    caption=f"{course.title}\n{course.description}",
                    reply_markup=get_callback_buttons(
                        btns={
                            "Удалить": f"delete_{course.pk}", "update": f"update_{course.pk}"
                        }                    )
                )
        else:
            await message.answer(text="здесь ничего нет пока что")

    async def delete_course_callback(self, callback_query: CallbackQuery, keyboard):
        course_id = callback_query.data.split("_")[-1]
        await self.delete_one(pk=int(course_id))
        await callback_query.answer(text="Курс был удален", show_alert=True)
        await callback_query.message.answer(text="Курс был удален", reply_markup=keyboard)
    #
    # async def update_callback(self, callback_query: CallbackQuery, keyboard):
    #     course_id = callback_query.data.split("_")[-1]
    #     update_data = await self.get_one(pk=int(course_id))
    #     UpdateCourse.for_update = update_data
    #     await callback_query.message.answer(text="Выберите что вы хотите обновить", reply_markup=keyboard)
    #
    # @classmethod
    # async def start_update_title(
    #         cls,
    #         message: Message,
    #         state: FSMContext,
    # ):
    #     await state.set_state(UpdateCourse.title)
    #     await message.answer(text=f"Отправьте мне новый загаловок")
    #
    # async def update_title(self, message: Message, state: FSMContext):
    #     await state.update_data(title=message.text)
    #     title = await state.get_data()
    #     await self.edit_one(pk=UpdateCourse.for_update.pk, data={"title": title})
    #     await state.clear()
    #     UpdateCourse.for_update = None
    #
    # @classmethod
    # async def start_update_description(
    #         cls,
    #         message: Message,
    #         state: FSMContext,
    # ):
    #     await state.set_state(UpdateCourse.description)
    #     await message.answer(text=f"Отправьте мне новое описание")
    #
    # async def update_description(self, message: Message, state: FSMContext):
    #     await state.update_data(description=message.text)
    #     description = await state.get_data()
    #     await self.edit_one(pk=UpdateCourse.for_update.pk, data={"description": description})
    #     await state.clear()
    #     UpdateCourse.for_update = None
    #
    # @classmethod
    # async def start_update_media(
    #         cls,
    #         message: Message,
    #         state: FSMContext,
    # ):
    #     await state.set_state(UpdateCourse.media_url)
    #     await message.answer(text=f"Отправьте мне новое фото")
    #
    # async def update_media(self, message: Message, state: FSMContext):
    #     await state.update_data(media_url=message.photo[-1].file_id)
    #     media = await state.get_data()
    #     await self.edit_one(pk=UpdateCourse.for_update.pk, data={"media_url": media})
    #     await state.clear()
    #     UpdateCourse.for_update = None

    @classmethod
    async def start_add_new_course(cls, message: Message, state: FSMContext):
        await message.answer(text="пришлите мне новое название", reply_markup=ReplyKeyboardRemove())
        await state.set_state(AddCourse.title)

    @classmethod
    async def add_title(cls, message: Message, state: FSMContext):
        await state.update_data(title=message.text)
        await message.answer(text="А теперь пришлите мне описание")
        await state.set_state(AddCourse.description)

    @classmethod
    async def add_description(cls, message: Message, state: FSMContext):
        await state.update_data(description=message.text)
        await message.answer(text="Хорошо, отправьте мне изображение")
        await state.set_state(AddCourse.media_url)

    async def add_media(self, message: Message, state: FSMContext, keyboard):
        await state.update_data(media_url=message.photo[-1].file_id)
        await message.answer(text='Окей курс был добавлен', reply_markup=keyboard)
        data = await state.get_data()
        await self.add_one(data=data)
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

        if current_state == AddCourse.title:
            await message.answer(
                "Предыдущего шага нет, или отправьте сообщение 'отмена'!"
            )
            return

        previous = None
        for step in AddCourse.__all_states__:
            if step.state == current_state:
                await state.set_state(previous)
                await message.answer(
                    f"Хорошо, вы  вернулсь к предыдущему шагу\n {AddCourse.texts[previous.state]}"
                )
                return
            previous = step


class CourseForUsersInterface(UsersInterface):
    model = Course

    async def send_all_courses(self, message: Message):
        course_list = await self.get_all()
        if course_list:
            for course in course_list:
                await message.answer_photo(
                    photo=course.media_url,
                    caption=f"{course.title}\n{course.description}"
                )
        else:
            await message.answer(text="здесь ничего нет пока что")
