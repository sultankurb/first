from src.handlers.crud.courses.interface import CourseForUsersInterface
from src.handlers.crud.events import UsersEventsInterface
from aiogram.filters import CommandStart, Command
from src.database.models.users import UsersModel
from src.handlers.crud.users import UsersManager
from aiogram.types import Message, CallbackQuery
from aiogram import Router, F


users = Router()
course_user_interface = CourseForUsersInterface()
event_user_interface = UsersEventsInterface()
manager = UsersManager()


@users.message(CommandStart())
async def hello_user_handler(message: Message):
    await message.answer(
        text=f"Ассалаўма алейкум {message.from_user.full_name}"
    )
    await manager.check_user(
        data=UsersModel(
            username=message.from_user.username,
            first_name=message.from_user.first_name,
            last_name=message.from_user.last_name,
            users_id=message.from_user.id,

        ).model_dump(exclude_unset=True),
        users_id=message.from_user.id
    )


@users.message(Command("courses"))
async def courses_list(message: Message):
    await course_user_interface.send_all_courses(message=message)


@users.callback_query(F.data.startswith("coursesub_"))
async def subscribe_to_course(callback_query: CallbackQuery):
    await course_user_interface.subscribe_callback(callback_query=callback_query)


@users.message(Command("events"))
async def courses_list(message: Message):
    await event_user_interface.send_all(message=message)
