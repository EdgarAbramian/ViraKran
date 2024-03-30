import asyncio
import pandas as pd

from backend.DataBase.database import Database


class BrandDb(Database):

    def __init__(self):
        super().__init__()
        asyncio.get_event_loop().run_until_complete(super().connect())

    async def select(self, brand: str = None):
        if brand:
            await self.cursor.execute("SELECT * FROM crane_brand WHERE brand=(%s)", (brand,))
        else:
            await self.cursor.execute("SELECT * FROM crane_brand")
        data = await self.cursor.fetchall()
        data = pd.DataFrame(data, columns=['id', 'name', 'info'])
        return data

    async def insert(self, values: tuple):
        await self.cursor.execute("INSERT INTO crane_brand(brand, info) VALUES (%s, %s)", values)

    async def delete(self, values: tuple):
        await self.cursor.execute("DELETE FROM crane_brand WHERE brand=(%s)", values)

    async def update(self, brand: str, info: str):
        await self.cursor.execute("UPDATE crane_brand SET info=(%s) WHERE brand=(%s)", (info, brand))


if __name__ == "__main__":
    db = BrandDb()
    res = asyncio.get_event_loop().run_until_complete(db.update("test", '1111111111111111'))
    print(res)
