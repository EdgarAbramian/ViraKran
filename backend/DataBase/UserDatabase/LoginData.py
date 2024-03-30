import asyncio
import pandas as pd

from backend.DataBase.database import Database


class UserLoginData(Database):
    def __init__(self):
        super().__init__()
        asyncio.get_event_loop().run_until_complete(super().connect())

    async def select(self, user_id):
        await self.cursor.execute("SELECT * FROM login_data where id=(%s)", (user_id,))
        data = await self.cursor.fetchall()
        data = pd.DataFrame(data, columns=['user_id', 'username', 'pass'])
        return data

    async def insert(self, values: tuple):
        await self.cursor.execute("INSERT INTO login_data(user_id, username_hash, pass_hash)"
                                  " VALUES (%s, %s, %s)", values)
        return True

    async def update(self, user_id: int, username: str = None, passw: str = None):
        if username and passw:
            await self.cursor.execute("UPDATE login_data SET username_hash=(%s), pass_hash=(%s) "
                                      "WHERE user_id=(%s)", (username, passw, user_id))
        if username:
            await self.cursor.execute("UPDATE login_data SET username_hash=(%s) "
                                      "WHERE user_id=(%s)", (username, user_id))
        if passw:
            await self.cursor.execute("UPDATE login_data SET pass_hash=(%s) "
                                      "WHERE user_id=(%s)", (passw, user_id))
        return True

    async def delete(self, user_id: int = None):
        await self.cursor.execute("DELETE FROM login_data WHERE id=(%s)", (user_id,))
        return True


if __name__ == "__main__":
    db = UserLoginData()
    res = asyncio.get_event_loop().run_until_complete(db.insert(('test', 'test', 'test', 'test')))
    print(res)
