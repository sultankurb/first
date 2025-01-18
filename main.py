from src.handlers.users.router import users
from src.handlers.admin.router import admin
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from src.settings import settings
import logging
import asyncio
import sys


dp = Dispatcher()
bot = Bot(token=settings.BOT_TOKEN)
bot.my_admins_list = [settings.ADMIN_ID, settings.ADMIN_2_ID]
logging.basicConfig(
    level=logging.INFO,
    stream=sys.stdout,
    format="%(asctime)s %(levelname)s:%(message)s",
)
dp.include_router(admin)
dp.include_router(users)


@dp.message(Command("start"))
async def hello_world(message: types.Message):
    await message.answer(text=f"Ассалаўма алейкум {message.from_user.full_name}")
    logging.info(msg=f"User with id={message.from_user.id} start delay with my bot")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
