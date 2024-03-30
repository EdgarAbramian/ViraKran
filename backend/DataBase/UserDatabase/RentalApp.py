import asyncio
import pandas as pd

from backend.DataBase.database import Database


class RentalApp(Database):
    def __init__(self):
        super().__init__()
        asyncio.get_event_loop().run_until_complete(super().connect())

    async def select(self):
        await self.cursor.execute("SELECT * FROM rental_application")
        data = await self.cursor.fetchall()
        data = pd.DataFrame(data, columns=['id', 'user_id', 'machinery_id', 'user_msg'])
        return data

    async def insert(self, values: tuple):
        await self.cursor.execute("INSERT INTO rental_application(user_id, machinery_id, user_msg)"
                                  " VALUES (%s, %s, %s)", values)
        return True


if __name__ == "__main__":
    db = RentalApp()
    res = asyncio.get_event_loop().run_until_complete(db.insert(('test', 'test', 'test', 'test')))
    print(res)
