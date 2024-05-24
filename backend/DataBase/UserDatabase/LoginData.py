import asyncio
import pandas as pd

from backend.DataBase.database import Database
from backend.models.DatabaseModels.Models import SelectUser, UserLoginForm, UpdtUser


class UserLoginData(Database):
    def __init__(self):
        super().__init__()
        asyncio.get_event_loop().run_until_complete(super().connect())

    async def select(self, user: SelectUser):
        """
        Execute a SELECT query to retrieve user data based on the user_id.

        Args:
            user (SelectUser): The ID of the user for data retrieval.

        Returns:
            pd.DataFrame: A DataFrame containing the retrieved user data with columns ['user_id', 'username', 'pass'].
        """
        await self.connect()
        try:
            if user.id:
                await self.cursor.execute("SELECT * FROM login_data where id=(%s)", (user.id,))
            elif user.username:
                await self.cursor.execute("SELECT * FROM login_data where username_hash=(%s)", (user.username,))
            else:
                await self.cursor.execute("SELECT * FROM login_data")

            data = await self.cursor.fetchall()
            data = pd.DataFrame(data, columns=['id', 'username', 'pass'])
            return data.to_json(orient='records')
        except Exception as e:
            return {'error': str(e)}

    async def insert(self, user: UserLoginForm):
        """
        Inserts a new record into the login_data table with the provided values.

        Args:
            user (UserLoginForm): A tuple containing the values to be inserted.

        Returns:
            bool: True if the insertion was successful.
        """
        await self.connect()

        try:
            await self.cursor.execute("INSERT INTO login_data(username_hash, pass_hash)"
                                      " VALUES (%s, %s)", (user.username, user.password))
            return True
        except Exception as e:
            return {'error': str(e)}

    async def update(self, user: UpdtUser):
        """
        Update user data in the database.

        Args:
            user (UpdtUser, optional): The new username. Defaults to None.

        Returns:
            bool: True if the update was successful.
        """
        await self.connect()

        try:
            if user.username:
                await self.cursor.execute(
                    f"UPDATE login_data SET username_hash='{user.username}', pass_hash='{user.passw}' WHERE username_hash='{user.username}'")
            return True
        except Exception as e:
            return {'error': str(e)}

    async def delete(self, username: str):

        await self.connect()

        try:
            await self.cursor.execute("DELETE FROM login_data WHERE username_hash=(%s)", (username,))
            return True
        except Exception as e:
            return {'error': str(e)}
