import asyncio
import pandas as pd

from backend.DataBase.database import Database
from backend.models.DatabaseModels.Models import MailingList


class CustListDb(Database):
    def __init__(self):
        super().__init__()
        asyncio.get_event_loop().run_until_complete(super().connect())

    async def select(self):
        await self.cursor.execute("SELECT * FROM mailing_list")
        data = await self.cursor.fetchall()
        data = pd.DataFrame(data, columns=['id', 'company_name', 'email', 'comp_info', 'comments'])
        return data

    async def insert(self, values: MailingList):
        model = (values.dict())
        values = ''
        fields = ''
        for val in model:
            if model[val]:
                fields += f" {val},"
                if type(model[val]) is int:
                    values += f" {model[val]},"
                else:
                    values += f" '{model[val]}',"
        values, fields = values[:-1], fields[:-1]
        _SQL = f'INSERT INTO mailing_list({fields}) VALUES({values})'
        await self.cursor.execute(_SQL)

    async def delete(self, mailing_list: MailingList):
        if mailing_list.id:
            await self.cursor.execute("DELETE FROM mailing_list WHERE id=(%s)", (mailing_list.id,))
        elif mailing_list.company_name:
            await self.cursor.execute("DELETE FROM mailing_list WHERE company_name=(%s)", (mailing_list.company_name,))
        else:
            raise ValueError("c_id or comp_name must be provided")
        return True


if __name__ == "__main__":
    db = CustListDb()
    cr = MailingList(company_name='test', email='test', comp_info='test', comments='test')
    res = asyncio.get_event_loop().run_until_complete(db.insert(cr))
    print(res)
