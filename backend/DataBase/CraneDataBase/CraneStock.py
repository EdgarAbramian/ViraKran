import asyncio
import pandas as pd

from backend.DataBase.database import Database
from backend.models.DatabaseModels.Models import CranStock


class CraneStock(Database):

    def __init__(self):
        super().__init__()
        asyncio.get_event_loop().run_until_complete(super().connect())

    async def select(self):
        await self.cursor.execute("SELECT * FROM crane_brand")
        data = await self.cursor.fetchall()
        data = pd.DataFrame(data, columns=['id', 'model_id', 'coordinates', 'on_the_go', 'info'])
        return data

    async def insert(self, crane_stock: CranStock):
        await self.cursor.execute("INSERT INTO crane_stock(model_id, coordinates, on_the_go, info) "
                                  "VALUES (%s, %s,%s, %s)", (crane_stock.MODEL_ID, crane_stock.coordinates, crane_stock.on_the_go, crane_stock.info))

    async def delete(self, crane_stock: CranStock):
        await self.cursor.execute("DELETE FROM crane_stock WHERE model_id=(%s)", (crane_stock.MODEL_ID,))

    async def update(self, crane_stock: CranStock):
        try:
            model = (crane_stock.dict())
            values = ''
            fields = ''
            for val in model:
                if model[val] and val != "MODEL_ID":

                    if type(model[val]) is int:
                        values += f"{val} = {model[val]},"
                    else:
                        values += f"{val} = '{model[val]}',"
            values, fields = values[:-1], fields[:-1]
            _SQL = f'UPDATE crane_stock SET {values} WHERE model = "{crane_stock.MODEL_ID}"'
            await self.cursor.execute(_SQL)

        except Exception as e:
            print(e)


if __name__ == "__main__":
    db = CraneStock()
    cr = CranStock(MODEL_ID=6, coordinates="2,3,4,5", on_the_go=True, info='')
    res = asyncio.get_event_loop().run_until_complete(db.insert(cr))
    print(res)
