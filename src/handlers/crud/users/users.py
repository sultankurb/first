from src.settings import async_session_maker, settings
from src.utils.crud import insert_one
from src.database.models import User
from sqlalchemy import select
from typing import Optional


class UsersManager:
    model = User

    async def select_user_by(
            self,
            users_id: Optional[int] = None
    ):
        async with async_session_maker() as session:
            stmt = select(self.model).filter_by(users_id=users_id)
            result = await session.execute(stmt)
            return result.scalar()

    async def add_user(self, data: dict):
        await insert_one(model=self.model, data=data)

    async def check_user(self, data: dict, users_id: int) -> None:
        user = await self.select_user_by(users_id=users_id)
        if user is None:
            if users_id == settings.ADMIN_ID:
                data.update(is_admin=True)
            await self.add_user(data=data)
