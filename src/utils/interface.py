from .crud import select_all, select_one, insert_one, delete_one, update_one
from src.database import Base


class AdminInterface:
    model: Base = None

    async def get_all(self):
        data = await select_all(model=self.model)
        return data

    async def get_one(self, pk: int):
        data = await select_one(model=self.model, pk=pk)
        return data

    async def add_one(self, data: dict):
        await insert_one(model=self.model, data=data)

    async def delete_one(self, pk: int):
        await delete_one(model=self.model, pk=pk)

    async def edit_one(self, pk: int, data: dict):
        await update_one(model=self.model, data=data, pk=pk)


class UsersInterface:
    model: Base = None

    async def get_all(self):
        data = await select_all(model=self.model)
        return data
