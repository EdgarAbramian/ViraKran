import asyncio
import pandas as pd

from backend.DataBase.database import Database


class UserDb(Database):
    def __init__(self):
        super().__init__()
        asyncio.get_event_loop().run_until_complete(super().connect())

    async def select(self):
        await self.cursor.execute("SELECT * FROM user")
        data = await self.cursor.fetchall()
        data = pd.DataFrame(data, columns=['id', 'name', 'surname', 'role', 'info'])
        return data

    async def insert(self, values: tuple):
        await self.cursor.execute("INSERT INTO user(name, surname, role, info)"
                                  " VALUES (%s, %s, %s, %s)", values)
        return True

    async def delete(self, user_id: int = None):
        if user_id:
            await self.cursor.execute("DELETE FROM user WHERE id=(%s)", (user_id,))
        return True

    async def update(self, user_id: int, values: tuple):
        await self.cursor.execute("UPDATE user SET name=(%s), surname=(%s), role=(%s), info=(%s) "
                                  "WHERE id=(%s)", (user_id, ))


if __name__ == "__main__":
    db = UserDb()
    res = asyncio.get_event_loop().run_until_complete(db.insert(('test', 'test', 'test', 'test')))
    print(res)
