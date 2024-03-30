import asyncio
import pandas as pd

from backend.DataBase.database import Database


class ModelDb(Database):

    def __init__(self):
        super().__init__()
        asyncio.get_event_loop().run_until_complete(super().connect())

    async def select(self, model: str = None, brand: str = None):
        if model:
            await self.cursor.execute("SELECT * FROM crane_model WHERE model=(%s)", (model,))
        elif brand:
            model_id = (await self.cursor.execute("SELECT id FROM crane_brand WHERE brand=(%s)", (brand,)))
            await self.cursor.execute("SELECT * FROM crane_model WHERE brand_id=(%s)", (model_id,))
        else:
            await self.cursor.execute("SELECT * FROM crane_model")

        data = await self.cursor.fetchall()
        data = pd.DataFrame(data, columns=['id', 'brand_id', 'model', 'description'])
        return data

    async def insert(self, values: tuple):
        await self.cursor.execute("INSERT INTO crane_model VALUES ('%s', '%s', '%s', '%s')", values)

    async def delete(self, values: tuple):
        await self.cursor.execute("DELETE FROM crane_model WHERE model=(%s)", values)

    async def update(self, model: str, info: str):
        await self.cursor.execute("UPDATE crane_model SET description=(%s) WHERE model=(%s)", (info, model))


if __name__ == "__main__":
    db = ModelDb()
    res = asyncio.get_event_loop().run_until_complete(db.select())
    print(res)
