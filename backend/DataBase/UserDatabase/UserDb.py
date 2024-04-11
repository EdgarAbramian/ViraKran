import asyncio
import pandas as pd

from backend.DataBase.database import Database
from backend.models.DatabaseModels.Models import User


class UserDb(Database):
    def __init__(self):
        super().__init__()
        asyncio.get_event_loop().run_until_complete(super().connect())

    async def select(self):
        await self.cursor.execute("SELECT * FROM user")
        data = await self.cursor.fetchall()
        data = pd.DataFrame(data, columns=['id', 'name', 'surname', 'role', 'info'])
        return data

    async def insert(self, user: User):
        await self.cursor.execute("INSERT INTO user(name, surname, role, info)"
                                  " VALUES (%s, %s, %s, %s)",
                                  (user.name, user.surname, user.role, user.info))
        return True

    async def delete(self, user_id: int):
        if user_id:
            await self.cursor.execute("DELETE FROM user WHERE id=(%s)", (user_id,))
        return True

    async def update(self, user: User):
        try:
            model = (user.dict())
            values = ''
            fields = ''
            for val in model:
                if model[val] and val != "id":

                    if type(model[val]) is int:
                        values += f"{val} = {model[val]},"
                    else:
                        values += f"{val} = '{model[val]}',"
            values, fields = values[:-1], fields[:-1]
            _SQL = f'UPDATE user SET {values} WHERE id = "{user.id}"'
            await self.cursor.execute(_SQL)

        except Exception as e:
            print(e)


if __name__ == "__main__":
    db = UserDb()
    res = asyncio.get_event_loop().run_until_complete(db.insert(('test', 'test', 'test', 'test')))
    print(res)
