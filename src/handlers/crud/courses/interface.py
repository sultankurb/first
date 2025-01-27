from .states import (
    AddCourse,
    UpdatePriceCourses,
    UpdateDescriptionCourses,
    UpdateTitleCourses,
    UpdateMediaCourses
)
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from src.keyboards.in_line import get_callback_buttons
from src.utils import AdminInterface, UsersInterface
from aiogram.fsm.context import FSMContext
from src.database.models import Course


class CourseInterfaceAdmin(AdminInterface):
    model = Course

    async def send_all_courses(self, message: Message):
        course_list = await self.get_all()
        if course_list:
            for course in course_list:
                await message.answer_photo(
                    photo=course.media_url,
                    caption=f"{course.title}\n{course.description}\n{course.price}",
                    reply_markup=get_callback_buttons(
                        btns={
                            "Удалить": f"coursedelete_{course.pk}",
                            "обновить заголовок": f"coursetitle_{course.pk}",
                            "обновите описание": f"coursedescription_{course.pk}",
                            "обновите фотографию": f"coursemedia_{course.pk}",
                            "обновите цену": f'courseprice_{course.pk}'
                        }
                    )
                )
        else:
            await message.answer(text="здесь ничего нет пока что")

    async def delete_course_callback(self, callback_query: CallbackQuery, keyboard):
        course_id = callback_query.data.split("_")[-1]
        await self.delete_one(pk=int(course_id))
        await callback_query.answer(text="Курс был удален", show_alert=True)
        await callback_query.message.answer(text="Курс был удален", reply_markup=keyboard)

    async def update_title_callback(self, callback_query: CallbackQuery, state: FSMContext):
        course_id = callback_query.data.split("_")[-1]
        data = await self.get_one(pk=int(course_id))
        UpdateTitleCourses.for_update = data
        await state.set_state(UpdateTitleCourses.title_courses)
        await callback_query.message.answer(
            text="Пришлите, пожалуйста, новое название",
            reply_markup=ReplyKeyboardRemove()
        )


    async def update_title(self, state: FSMContext, message: Message, keyboard):
        await state.update_data(title=message.text)
        data = await state.get_data()
        await self.edit_one(pk=UpdateTitleCourses.for_update.pk, data=data)
        await message.answer(text="название было обновлено", reply_markup=keyboard)
        await state.clear()
        UpdateTitleCourses.for_update = None

    async def update_description_callback(self, callback_query: CallbackQuery, state: FSMContext):
        course_id = callback_query.data.split("_")[-1]
        data = await self.get_one(pk=int(course_id))
        UpdateDescriptionCourses.for_update = data
        await state.set_state(UpdateDescriptionCourses.description_Courses)
        await callback_query.message.answer(
            text="Пришлите, пожалуйста, новое описание",
            reply_markup=ReplyKeyboardRemove()
        )

    async def update_description(self, state: FSMContext, message: Message, keyboard):
        await state.update_data(description=message.text)
        data = await state.get_data()
        await self.edit_one(pk=UpdateDescriptionCourses.for_update.pk, data=data)
        await message.answer(text="описание было обновлено", reply_markup=keyboard)
        await state.clear()
        UpdateDescriptionCourses.for_update = None

    async def update_media_callback(self, callback_query: CallbackQuery, state: FSMContext):
        course_id = callback_query.data.split("_")[-1]
        data = await self.get_one(pk=int(course_id))
        UpdateMediaCourses.for_update = data
        await state.set_state(UpdateMediaCourses.media_url_courses)
        await callback_query.message.answer(
            text="пришлите, пожалуйста, новую фотографию",
            reply_markup=ReplyKeyboardRemove()
        )

    async def update_media(self, state: FSMContext, message: Message, keyboard):
        await state.update_data(media_url=message.photo[-1].file_id)
        data = await state.get_data()
        await self.edit_one(pk=UpdateMediaCourses.for_update.pk, data=data)
        await message.answer(text="фотография была обновлена", reply_markup=keyboard)
        await state.clear()
        UpdateMediaCourses.for_update = None

    async def update_price_callback(self, state: FSMContext, callback_query: CallbackQuery):
        course_pk = callback_query.data.split("_")[-1]
        data = await self.get_one(pk=int(course_pk))
        UpdatePriceCourses.for_update = data
        await state.set_state(UpdatePriceCourses.price_courses)
        await callback_query.message.answer(
            text="пришлите, пожалуйста, новую цену",
            reply_markup=ReplyKeyboardRemove()
        )

    async def update_price(self, message: Message, state: FSMContext, keyboard):
        await state.update_data(price=int(message.text))
        data = await state.get_data()
        await message.answer(text='цена была обновлена', reply_markup=keyboard)
        await self.edit_one(pk=UpdatePriceCourses.for_update.pk, data=data)
        await state.clear()
        UpdatePriceCourses.for_update = None



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

    @classmethod
    async def add_media(cls, message: Message, state: FSMContext):
        await state.update_data(media_url=message.photo[-1].file_id)
        await message.answer(text='Окей, пришлите мне цену')
        await state.set_state(AddCourse.price)

    async def add_price(self, message: Message, state: FSMContext, keyboard):
        await state.update_data(price=int(message.text))
        data = await state.get_data()
        print(data)
        await self.add_one(data=data)
        await state.clear()
        await message.answer(text="Курс был добавлен", reply_markup=keyboard)

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
