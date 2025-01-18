from src.database.crud.courses import CoursesRepository
from src.database.crud.events import EventsRepository
from src.database.crud.posts import PostsRepository
from src.filters.chat_types import ChatTypeFilter
from aiogram.filters import Command
from aiogram.types import Message
from aiogram import Router


users = Router()
users.message.filter(ChatTypeFilter(chat_types=["private"]))
course_repo = CoursesRepository()
events_repo = EventsRepository()
posts_repo = PostsRepository()


@users.message(Command("courses"))
async def show_courses(message: Message):
    courses_list = await course_repo.select_all()
    if courses_list:
        for course in courses_list:
            await message.answer_photo(
                photo=course.images_url, caption=f"{course.title}\n{course.description}"
            )
    else:
        await message.answer(text="Здесь пока ничего нету")


@users.message(Command("posts"))
async def show_posts(message: Message):
    posts_list: list = await posts_repo.select_all()
    if posts_list:
        for post in posts_list:
            await message.answer_photo(
                photo=post.media_url, caption=f"{post.title}\n{post.description}"
            )
    else:
        await message.answer(text="Здесь пока ничего нету")


@users.message(Command("events"))
async def sow_events(message: Message):
    events_list = await events_repo.filtered_search()
    if events_list:
        for event in events_list:
            await message.answer_photo(
                photo=event.media_url, caption=f"{event.title}\n{event.description}"
            )
    else:
        await message.answer(text="Здесь пока ничего нету")
