import pandas as pd

from backend.DataBase.database import Database
from backend.models.DatabaseModels.Models import CranStockModel


class CraneStock(Database):

    def __init__(self):
        super().__init__()

    async def select(self, crane_stock: CranStockModel):
        """
        Execute a SELECT query to retrieve all records from the crane_brand table.

        Returns:
        pd.DataFrame: A DataFrame containing the retrieved records.
        """
        await self.connect()
        try:
            if crane_stock.id is not None:
                await self.cursor.execute("SELECT * FROM crane_stock WHERE id=(%s)", (crane_stock.model_id,))
            elif crane_stock.model_id is not None:
                await self.cursor.execute("SELECT * FROM crane_stock WHERE model_id=(%s)", (crane_stock.model_id,))
            elif crane_stock.on_the_go is not None:
                await self.cursor.execute("SELECT * FROM crane_stock WHERE on_the_go=(%s)", (crane_stock.on_the_go,))
            else:
                await self.cursor.execute("SELECT * FROM crane_stock")
            data = await self.cursor.fetchall()
            data = pd.DataFrame(data, columns=['id', 'model_id', 'coordinates', 'on_the_go', 'info'])
            return data.to_json(orient='records')
        except Exception as e:
            return {'error': str(e)}

    async def insert(self, crane_stock: CranStockModel):
        """
        Inserts a CraneStock object into the database.

        Args:
            crane_stock (CraneStock): The CraneStock object to be inserted.
        """
        await self.connect()
        try:
            await self.cursor.execute("INSERT INTO crane_stock(model_id, coordinates, on_the_go, info) "
                                      "VALUES (%s, %s,%s, %s)",
                                      (crane_stock.model_id, crane_stock.coordinates, crane_stock.on_the_go,
                                       crane_stock.info))
            return True
        except Exception as e:
            return {'error': str(e)}

    async def delete(self, crane_stock: CranStockModel):
        """
        Delete a specific crane stock record from the database based on the model ID.

        Args:
            crane_stock (CranStockModel): The crane stock object to be deleted.
        """
        await self.connect()
        try:
            if crane_stock.id:
                await self.cursor.execute("DELETE FROM crane_stock WHERE id=(%s)", (crane_stock.id,))
            elif crane_stock.model_id is not None:
                await self.cursor.execute("DELETE FROM crane_stock WHERE model_id=(%s)", (crane_stock.model_id,))
            elif crane_stock.on_the_go is not None:
                await self.cursor.execute("DELETE FROM crane_stock WHERE on_the_go=(%s)", (crane_stock.on_the_go,))
            await self.cursor.execute("COMMIT;")
            return True
        except Exception as e:
            return {'error': str(e)}

    async def update(self, crane_stock: CranStockModel):
        """
        Update the crane stock record in the database based on the provided CraneStock object.

        Args:
            crane_stock (CranStockModel): The CraneStock object containing the updated values.

        """
        await self.connect()

        try:
            # Convert CraneStock object to a dictionary
            model = (crane_stock.dict())
            values = ''
            print(model)
            # Iterate over the model dictionary
            for val in model:
                if (model[val] and val != "model_id") or type(model[val]) is bool:

                    if type(model[val]) is str:
                        print(type(model[val]))
                        values += f"{val} = '{model[val]}',"
                    elif type(model[val]) is bool:
                        values += f"{val} = {model[val]},"

            # Remove the trailing comma from values
            values = values[:-1]

            # Construct the SQL query
            _SQL = f'UPDATE crane_stock SET {values} WHERE id="{crane_stock.id}"'

            # Execute the SQL query
            await self.cursor.execute(_SQL)

            return True

        except Exception as e:
            # Print any exceptions that occur during the update process
            return {'error': str(e)}
