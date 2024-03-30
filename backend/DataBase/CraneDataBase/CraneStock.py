import asyncio
import pandas as pd

from backend.DataBase.database import Database


class CraneStock(Database):

    def __init__(self):
        super().__init__()
        asyncio.get_event_loop().run_until_complete(super().connect())

    async def select(self, on_the_go: bool = False, model: str = None, coordinates: str = None):
        if model:
            model_id = await self.cursor.execute("SELECT * FROM crane_model WHERE model=(%s)", (model,))
            if on_the_go and coordinates:
                await self.cursor.execute(
                    "SELECT * FROM crane_stock "
                    "WHERE model_id=(%s) AND on_the_go=(%s) AND coordinates=(%s)",
                    (model_id, on_the_go, coordinates))
            if on_the_go:
                await self.cursor.execute("SELECT * FROM crane_stock "
                                          "WHERE model_id=(%s) AND on_the_go=(%s)", (on_the_go, ))
            else:
                await self.cursor.execute("SELECT * FROM crane_stock WHERE model_id=(%s)", (model_id,))
        elif on_the_go:
            await self.cursor.execute("SELECT * FROM crane_stock WHERE on_the_go=(%s)", (on_the_go,))
        elif coordinates:
            await self.cursor.execute("SELECT * FROM crane_stock WHERE coordinates=(%s)", (coordinates,))
        else:
            await self.cursor.execute("SELECT * FROM crane_brand")
        data = await self.cursor.fetchall()
        data = pd.DataFrame(data, columns=['id', 'model_id', 'coordinates', 'on_the_go', 'info'])
        return data

    async def insert(self, values: tuple):
        await self.cursor.execute("INSERT INTO crane_stock(model_id, coordinates, on_the_go, info) "
                                  "VALUES (%s, %s,%s, %s)", values)

    async def delete(self, model_id: int):
        await self.cursor.execute("DELETE FROM crane_brand WHERE brand=(%s)", (model_id, ))

    async def update(self, model_id: int, on_the_go: bool, coordinates: str, info: str):
        await self.cursor.execute("UPDATE crane_stock SET coordinates=(%s), on_the_go=(%s), info=(%s) "
                                  "WHERE model_id=(%s)", (coordinates, on_the_go, info))


if __name__ == "__main__":
    db = CraneStock()
    res = asyncio.get_event_loop().run_until_complete(db.select(model="CTT 191-10 TS21", on_the_go=False))
    print(res)
