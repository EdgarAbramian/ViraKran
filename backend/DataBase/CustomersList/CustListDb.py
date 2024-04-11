import asyncio
import pandas as pd

from backend.DataBase.database import Database
from backend.models.DatabaseModels.Models import MailingList


class CustListDb(Database):
    def __init__(self):
        super().__init__()
        asyncio.get_event_loop().run_until_complete(super().connect())

    async def select(self):
        """
        Execute a SELECT query to retrieve all records from the mailing_list table.

        Returns:
            pd.DataFrame: A DataFrame containing the retrieved records.
        """
        await self.cursor.execute("SELECT * FROM mailing_list")
        data = await self.cursor.fetchall()
        data = pd.DataFrame(data, columns=['id', 'company_name', 'email', 'comp_info', 'comments'])
        return data

    async def insert(self, values: MailingList):
        """
        Insert a new record into the mailing_list table based on the provided MailingList object.

        Args:
            values (MailingList): The MailingList object containing the values to insert.

        """
        model = (values.dict())
        values = ''
        fields = ''

        # Iterate over the model dictionary to build the values and fields strings
        for val in model:
            if model[val]:
                fields += f" {val},"
                if type(model[val]) is int:
                    values += f" {model[val]},"
                else:
                    values += f" '{model[val]}',"
        # Remove the trailing comma from values and fields
        values, fields = values[:-1], fields[:-1]

        # Construct the SQL query
        _SQL = f'INSERT INTO mailing_list({fields}) VALUES({values})'

        # Execute the SQL query
        await self.cursor.execute(_SQL)

    async def delete(self, mailing_list: MailingList):
        """
        Delete a record from the mailing_list table based on the provided MailingList object.

        Args:
            mailing_list (MailingList): The MailingList object containing the identifier for deletion.

        Raises:
            ValueError: If both the id and company_name fields are missing.

        Returns:
            bool: True if the record is successfully deleted.
        """
        if mailing_list.id:
            # Delete record based on id
            await self.cursor.execute("DELETE FROM mailing_list WHERE id=(%s)", (mailing_list.id,))
        elif mailing_list.company_name:
            # Delete record based on company name
            await self.cursor.execute("DELETE FROM mailing_list WHERE company_name=(%s)", (mailing_list.company_name,))
        else:
            # Raise an error if both id and company_name are missing
            raise ValueError("c_id or comp_name must be provided")
        return True


if __name__ == "__main__":
    db = CustListDb()
    cr = MailingList(company_name='test', email='test', comp_info='test', comments='test')
    res = asyncio.get_event_loop().run_until_complete(db.insert(cr))
    print(res)
