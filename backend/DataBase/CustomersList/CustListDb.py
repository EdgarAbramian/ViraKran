import asyncio
import pandas as pd

from backend.DataBase.database import Database


class CustListDb(Database):
    def __init__(self):
        super().__init__()
        asyncio.get_event_loop().run_until_complete(super().connect())

    async def select(self):
        await self.cursor.execute("SELECT * FROM customers_list")
        data = await self.cursor.fetchall()
        data = pd.DataFrame(data, columns=['id', 'company_name', 'email', 'comp_info', 'comments'])
        return data

    async def insert(self, values: tuple):
        await self.cursor.execute("INSERT INTO customers_list(company_name, email, comp_info, comments)"
                                  " VALUES (%s, %s, %s, %s)", values)
        return True

    async def delete(self, c_id: int = None, comp_name: str = None):
        if c_id:
            await self.cursor.execute("DELETE FROM customers_list WHERE id=(%s)", (c_id,))
        elif comp_name:
            await self.cursor.execute("DELETE FROM customers_list WHERE company_name=(%s)", (comp_name,))
        else:
            raise ValueError("c_id or comp_name must be provided")
        return True


if __name__ == "__main__":
    db = CustListDb()
    res = asyncio.get_event_loop().run_until_complete(db.insert(('test', 'test', 'test', 'test')))
    print(res)
