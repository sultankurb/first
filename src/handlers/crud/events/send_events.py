from src.settings import async_session_maker, settings
from src.utils.crud import update_one
from src.database.models import User
from sqlalchemy import select
from aiogram import Bot
import asyncio


async def get_users():
    async with async_session_maker() as session:
        stmt = select(User).filter_by(is_blocked=False)
        result = await session.execute(stmt)
        return result.scalars().all()


def send_event(new_data: dict, bot: Bot = Bot(token=settings.BOT_TOKEN)):
    users = asyncio.run(get_users())
    for user in users:
        try:
            bot.send_photo(
                chat_id=user.users_id,
                photo=new_data["media_url"],
                caption=f"{new_data["title"]}\n{new_data["description"]}"
            )
        except:
            update_one(model=User, pk=user.pk, data={"is_blocked": True})


async def send_events(new_data: dict, bot: Bot = Bot(token=settings.BOT_TOKEN)):
    users = await get_users()
    for user in users:
        await bot.send_photo(
            chat_id=user.users_id,
            photo=new_data["media_url"],
            caption=f"{new_data["title"]}\n{new_data["description"]}"
        )
