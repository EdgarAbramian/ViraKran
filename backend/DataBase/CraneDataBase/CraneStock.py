import asyncio
import pandas as pd

from backend.DataBase.database import Database
from backend.models.DatabaseModels.Models import CranStock


class CraneStock(Database):

    def __init__(self):
        super().__init__()
        asyncio.get_event_loop().run_until_complete(super().connect())

    async def select(self):
        """
        Execute a SELECT query to retrieve all records from the crane_brand table.

        Returns:
        pd.DataFrame: A DataFrame containing the retrieved records.
        """
        await self.cursor.execute("SELECT * FROM crane_brand")
        data = await self.cursor.fetchall()
        data = pd.DataFrame(data, columns=['id', 'model_id', 'coordinates', 'on_the_go', 'info'])
        return data

    async def insert(self, crane_stock: CranStock):
        """
        Inserts a CraneStock object into the database.

        Args:
            crane_stock (CraneStock): The CraneStock object to be inserted.
        """
        await self.cursor.execute("INSERT INTO crane_stock(model_id, coordinates, on_the_go, info) "
                                  "VALUES (%s, %s,%s, %s)",
                                  (crane_stock.MODEL_ID, crane_stock.coordinates, crane_stock.on_the_go,
                                   crane_stock.info))

    async def delete(self, crane_stock: CranStock):
        """
        Delete a specific crane stock record from the database based on the model ID.

        Args:
            crane_stock (CranStock): The crane stock object to be deleted.
        """
        await self.cursor.execute("DELETE FROM crane_stock WHERE model_id=(%s)", (crane_stock.MODEL_ID,))

    async def update(self, crane_stock: CranStock):
        """
        Update the crane stock record in the database based on the provided CraneStock object.

        Args:
            crane_stock (CranStock): The CraneStock object containing the updated values.

        """
        try:
            # Convert CraneStock object to a dictionary
            model = (crane_stock.dict())
            values = ''
            fields = ''

            # Iterate over the model dictionary
            for val in model:
                if model[val] and val != "MODEL_ID":
                    if type(model[val]) is int:
                        values += f"{val} = {model[val]},"
                    else:
                        values += f"{val} = '{model[val]}',"

            # Remove the trailing comma from values
            values, fields = values[:-1], fields[:-1]

            # Construct the SQL query
            _SQL = f'UPDATE crane_stock SET {values} WHERE model = "{crane_stock.MODEL_ID}"'

            # Execute the SQL query
            await self.cursor.execute(_SQL)

        except Exception as e:
            # Print any exceptions that occur during the update process
            print(e)


if __name__ == "__main__":
    db = CraneStock()
    cr = CranStock(MODEL_ID=6, coordinates="2,3,4,5", on_the_go=True, info='')
    res = asyncio.get_event_loop().run_until_complete(db.insert(cr))
    print(res)
