from src.database.models import CourseSub, User
from src.settings import async_session_maker
from sqlalchemy import select, insert
from src.settings import settings
from aiogram import Bot


async def get_users():
    async with async_session_maker() as session:
        stmt = select(User).filter_by(is_admin=True)
        result = await session.execute(stmt)
        return result.scalars().all()


async def sub_to_course(data: dict) -> None:
    async with async_session_maker() as session:
        stmt = insert(CourseSub).values(**data)
        await session.execute(stmt)
        await session.commit()



async def send_subscribe(data: dict, bot: Bot = Bot(token=settings.BOT_TOKEN)):
    users = await get_users()
    for user in users:
        await bot.send_message(
            chat_id=user.users_id,
            text=f"{data.get("username")}\n\n{data.get("fullname")} был подписан на курс"
        )
