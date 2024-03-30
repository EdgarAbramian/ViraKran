import asyncio

from UserDb import UserDb
from LoginData import UserLoginData
from RentalApp import RentalApp

__all__ = ['UserDb', 'UserLoginData', 'RentalApp']


class UserDatabase(object):

    def __init__(self):
        self.user = UserDb()
        self.login = UserLoginData()
        self.rentalApp = RentalApp()

    async def __aenter__(self):
        await self.user.connect()
        await self.login.connect()
        await self.rentalApp.connect()
        return self

    async def __aexit__(self):
        await self.user.disconnect()
        await self.login.disconnect()
        await self.rentalApp.disconnect()


if __name__ == "__main__":
    db = UserDatabase()
    res = asyncio.get_event_loop().run_until_complete(db.user.insert(('test', 'test', 'test', 'test')))
    print(res)
