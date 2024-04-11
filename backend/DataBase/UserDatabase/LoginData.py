import asyncio
import pandas as pd

from backend.DataBase.database import Database


class UserLoginData(Database):
    def __init__(self):
        super().__init__()
        asyncio.get_event_loop().run_until_complete(super().connect())

    async def select(self, user_id):
        """
        Execute a SELECT query to retrieve user data based on the user_id.

        Args:
            user_id (int): The ID of the user for data retrieval.

        Returns:
            pd.DataFrame: A DataFrame containing the retrieved user data with columns ['user_id', 'username', 'pass'].
        """
        await self.cursor.execute("SELECT * FROM login_data where id=(%s)", (user_id,))
        data = await self.cursor.fetchall()
        data = pd.DataFrame(data, columns=['user_id', 'username', 'pass'])
        return data

    async def insert(self, values: tuple):
        """
        Inserts a new record into the login_data table with the provided values.

        Args:
            values (tuple): A tuple containing the values to be inserted.

        Returns:
            bool: True if the insertion was successful.
        """
        await self.cursor.execute("INSERT INTO login_data(user_id, username_hash, pass_hash)"
                                  " VALUES (%s, %s, %s)", values)
        return True

    async def update(self, user_id: int, username: str = None, passw: str = None):
        """
        Update user data in the database.

        Args:
            user_id (int): The ID of the user to update.
            username (str, optional): The new username. Defaults to None.
            passw (str, optional): The new password. Defaults to None.

        Returns:
            bool: True if the update was successful.
        """

        # Update both username and password
        if username and passw:
            await self.cursor.execute("UPDATE login_data SET username_hash=(%s), pass_hash=(%s) "
                                      "WHERE user_id=(%s)", (username, passw, user_id))
        # Update only username
        if username:
            await self.cursor.execute("UPDATE login_data SET username_hash=(%s) "
                                      "WHERE user_id=(%s)", (username, user_id))
        # Update only password
        if passw:
            await self.cursor.execute("UPDATE login_data SET pass_hash=(%s) "
                                      "WHERE user_id=(%s)", (passw, user_id))
        return True

    async def delete(self, user_id: int = None):
        """
        Deletes a user's login data from the database.

        Args:
            user_id (int): The ID of the user whose login data will be deleted.

        Returns:
            bool: True if the deletion was successful.
        """
        await self.cursor.execute("DELETE FROM login_data WHERE id=(%s)", (user_id,))
        return True


if __name__ == "__main__":
    db = UserLoginData()
    res = asyncio.get_event_loop().run_until_complete(db.insert(('test', 'test', 'test', 'test')))
    print(res)
