import asyncio
import pandas as pd

from backend.DataBase.database import Database
from backend.models.DatabaseModels.Models import User


class UserDb(Database):
    def __init__(self):
        super().__init__()
        asyncio.get_event_loop().run_until_complete(super().connect())

    async def select(self):
        """
        Executes a SELECT query on the 'user' table using the cursor.

        Returns:
        pd.DataFrame: A pandas DataFrame containing the results of the query.
        """
        await self.cursor.execute("SELECT * FROM user")
        data = await self.cursor.fetchall()
        data = pd.DataFrame(data, columns=['id', 'name', 'surname', 'role', 'info'])
        return data

    async def insert(self, user: User):
        """
        Inserts a new record into the 'user' table with the provided user details.

        Args:
            user (User): An instance of the User class containing the user details.

        Returns:
            bool: True if the insertion was successful.
        """
        await self.cursor.execute("INSERT INTO user(name, surname, role, info)"
                                  " VALUES (%s, %s, %s, %s)",
                                  (user.name, user.surname, user.role, user.info))
        return True

    async def delete(self, user_id: int):
        """
        Deletes a user's record from the 'user' table based on the user_id.

        Args:
            user_id (int): The ID of the user whose record will be deleted.

        Returns:
            bool: True if the deletion was successful.
        """
        if user_id:
            await self.cursor.execute("DELETE FROM user WHERE id=(%s)", (user_id,))
        return True

    async def update(self, user: User):
        """
        Update user data in the database based on the provided User object.

        Args:
            user (User): The User object containing the data to be updated.

        Raises:
            Exception: If an error occurs during the database update process.
        """

        try:
            # Convert User object to dictionary
            model = (user.dict())
            values = ''
            fields = ''
            # Iterate over the dictionary keys and values
            for val in model:
                # Check if the value is not empty and the key is not "id"
                if model[val] and val != "id":
                    # Check the type of the value and construct the update string accordingly
                    if type(model[val]) is int:
                        values += f"{val} = {model[val]},"
                    else:
                        values += f"{val} = '{model[val]}',"
            # Remove the extra comma at the end of the values string
            values = values[:-1]
            _SQL = f'UPDATE user SET {values} WHERE id = "{user.id}"'
            # Execute the SQL query
            await self.cursor.execute(_SQL)

        except Exception as e:
            # Print any exceptions that occur during the update process
            print(e)


if __name__ == "__main__":
    db = UserDb()
    res = asyncio.get_event_loop().run_until_complete(db.insert(('test', 'test', 'test', 'test')))
    print(res)
