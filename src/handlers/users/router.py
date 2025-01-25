from src.handlers.crud.courses.interface import CourseForUsersInterface
from aiogram.filters import CommandStart, Command
from src.database.models.users import UsersModel
from src.handlers.crud.users import UsersManager
from aiogram.types import Message
from aiogram import Router


users = Router()
interface = CourseForUsersInterface()
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
    await interface.send_all_courses(message=message)
