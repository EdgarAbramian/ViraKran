import asyncio
import pandas as pd

from backend.DataBase.database import Database
from backend.models.DatabaseModels.Models import CraneModel, CraneModelSelect, CraneModelDelete, CraneModelUpdate


class ModelDb(Database):

    def __init__(self):
        super().__init__()
        asyncio.get_event_loop().run_until_complete(super().connect())

    async def select(self, crane_model: CraneModelSelect):
        """
        Function selects data from the 'crane_model' table based on the criteria provided in the crane_model object.

        Args:
            crane_model (CraneModelSelect): An object containing the criteria for selecting data.

        Returns:
            str: JSON string representing the selected data records.
        """

        # Extract the model information from the CraneModelSelect object
        model_info = crane_model.dict()

        # Initialize the SQL columns string
        _SQL_COLUMNS = ""

        # Iterate through the model information to build the SQL WHERE clause
        for col in model_info:
            if type(model_info.get(col)) is str:
                _SQL_COLUMNS += "{}='{}' AND ".format(col, model_info.get(col)) if model_info.get(col) else ''
            else:
                _SQL_COLUMNS += "{}={} AND ".format(col, model_info.get(col)) if model_info.get(col) else ''

        # Remove the trailing 'AND ' and join the SQL columns
        _SQL_COLUMNS = ' '.join(_SQL_COLUMNS.split()[:-1])

        # Execute the SQL query to select data from the 'crane_model' table
        await self.cursor.execute(f"SELECT * FROM crane_model WHERE {_SQL_COLUMNS}")

        # Fetch the selected data
        data = await self.cursor.fetchall()

        # Create a DataFrame from the selected data
        df = pd.DataFrame(data, columns=CraneModel.model_fields)

        # Return the selected data in JSON format
        return df.to_json(orient='records')

    async def insert(self, crane_model: CraneModel):
        """
        Insert a new crane model into the database.

        Args:
            crane_model (CraneModel): The crane model object to insert.
        """

        # Convert crane_model to a dictionary
        model = (crane_model.dict())

        # Initialize empty strings for values and fields
        values = ''
        fields = ''

        # Iterate over the model dictionary
        for val in model:
            # Check if the value is not empty
            if model[val]:
                # Append the field name to the fields string
                fields += f" {val},"

                # Append the value to the values string
                if type(model[val]) is int:
                    values += f" {model[val]},"
                else:
                    values += f" '{model[val]}',"

        # Remove the trailing comma from values and fields
        values, fields = values[:-1], fields[:-1]

        # Construct the SQL query
        _SQL = f'INSERT INTO crane_model({fields}) VALUES({values})'

        # Execute the SQL query
        await self.cursor.execute(_SQL)

        return True

    async def delete(self, crane_model: CraneModelDelete):
        """
        Delete a crane model from the database based on the provided crane_model object.

        Args:
            crane_model (CraneModelDelete): The crane model object to delete.
        """
        try:
            # Start a transaction and set autocommit to 0
            await self.cursor.execute(
                f"START TRANSACTION; SET AUTOCOMMIT=0; "
                f"DELETE FROM crane_stock WHERE model_id IN "
                f"(SELECT id FROM crane_model WHERE model = '{crane_model.model}');"
                f"DELETE FROM crane_model WHERE model = '{crane_model.model}'"
            )
            await self.connection.commit()

            return True
        except Exception as e:
            # Rollback the transaction in case of an exception
            await self.connection.rollback()
            print(e)

    async def update(self, crane_model: CraneModelUpdate):
        """
        Update crane model in the database with the values provided in the CraneModelUpdate object.

        Args:
            crane_model: An instance of CraneModelUpdate containing the updated values for the crane model.

        """
        try:
            # Convert CraneModelUpdate object to a dictionary
            model = (crane_model.dict())
            values = ''
            fields = ''

            # Iterate over the dictionary and build the SET clause for the SQL query
            for val in model:
                if model[val] and val != "model":
                    if type(model[val]) is int:
                        values += f"{val} = {model[val]},"
                    else:
                        values += f"{val} = '{model[val]}',"

            # Remove the trailing comma from values
            values = values[:-1]

            # Construct the SQL query
            _SQL = f'UPDATE crane_model SET {values} WHERE model = "{crane_model.model}"'

            # Execute the SQL query
            await self.cursor.execute(_SQL)

            return True
        except Exception as e:
            # Log any exceptions that occur during the update process
            print(e)
            return False


if __name__ == "__main__":
    db = ModelDb()
    model = CraneModelSelect(model='tes1t')
    new_model = CraneModelUpdate(model='tesasdff', height_anker_C38=1.0, height_anker_C45=1.0, height_anker_C60=1.0)
    loop = asyncio.get_event_loop()
    model_info = loop.run_until_complete(db.update(new_model))
    print(model_info)
