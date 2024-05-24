import pandas as pd

from backend.DataBase.database import Database
from backend.models.DatabaseModels.Models import RentalApplication


class RentalApp(Database):
    def __init__(self):
        super().__init__()
        # asyncio.get_event_loop().run_until_complete(super().connect())

    async def select(self):
        """
        Selects all the records from the rental_application table and returns them as a pandas DataFrame.
        """
        try:
            await self.connect()

            await self.cursor.execute("SELECT * FROM rental_application")
            data = await self.cursor.fetchall()
            data = pd.DataFrame(data, columns=['id', 'machinery_id', 'user_msg', 'name',
                                               'surname', 'email', 'phone', 'status'])
            return data.to_json(orient='records')
        except Exception as e:
            return {'error': e}

    async def insert(self, RentApp: RentalApplication):
        """
        Insert a new rental application into the database.

        Args:
        RentApp (RentalApplication): The rental application to be inserted.

        Returns:
        bool: True if the insertion was successful, False otherwise.
        await self.connect()
        """
        try:
            await self.connect()

            await self.cursor.execute(
                "INSERT INTO rental_application(machinery_id, user_msg, name, email, phone, status)"
                " VALUES (%s, %s, %s, %s, %s, %s)", (RentApp.machinery_id, RentApp.user_msg, RentApp.name,
                                                     RentApp.email, RentApp.phone, RentApp.status))
            return True
        except Exception as e:
            print(e)
            return {'error': e}

    async def update(self, email: str, status: bool):
        """
        Update the status of a rental application based on the email.

        Args:
            email (str): The email of the rental application to update.
            status (bool): The new status value.

        Returns:
            bool: True if the update was successful.
        """
        try:
            await self.connect()
            await self.cursor.execute(f"UPDATE rental_application SET status = {status} WHERE email = '{email}'")
        except Exception as e:
            return {'error': e}
