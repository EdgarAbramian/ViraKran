import asyncio
import pandas as pd

from backend.DataBase.database import Database
from backend.models.DatabaseModels.Models import RentalApplication, RentalApplicationUser


class RentalApp(Database):
    def __init__(self):
        super().__init__()
        asyncio.get_event_loop().run_until_complete(super().connect())

    async def select(self):
        await self.cursor.execute("SELECT * FROM rental_application")
        data = await self.cursor.fetchall()
        data = pd.DataFrame(data, columns=['id', 'machinery_id', 'user_msg', 'name',
                                           'surname', 'email', 'phone', 'status'])
        return data

    async def insert(self, RentApp: RentalApplication):
        await self.cursor.execute(
            "INSERT INTO rental_application(machinery_id, user_msg, name, email, phone, status)"
            " VALUES (%s, %s, %s, %s, %s, %s)", (RentApp.machinery_id, RentApp.user_msg, RentApp.user_info.name,
                                                 RentApp.user_info.email,
                                                 RentApp.user_info.phone,
                                                 RentApp.status))
        return True

    async def update(self, email: str, status: bool):
        await self.cursor.execute(f"UPDATE rental_application SET status = {status} WHERE email = '{email}'")


if __name__ == "__main__":
    db = RentalApp()
    cr = RentalApplication(machinery_id=1, user_msg="test", user_info=RentalApplicationUser(name="test", email="test"),
                           status=True)
    res = asyncio.get_event_loop().run_until_complete(db.update('test', True))
    print(res)
