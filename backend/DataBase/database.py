import asyncio

import aiomysql
from backend.DataBase import settings


class Database:
    def __init__(self):
        self.loop = asyncio.get_event_loop()
        self.host = settings["Host"]
        self.user = settings["User"]
        self.password = settings["Password"]
        self.database = settings["Database"]
        self.port = settings["Port"]
        self.connection = None
        self.cursor = None

    async def connect(self):
        self.connection = await aiomysql.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            db=self.database,
            port=self.port,
            autocommit=True
        )
        self.connection.autocommit = True
        self.cursor = await self.connection.cursor()

        if self.connection:
            if self.cursor:
                print(f"Connected to MySQL database {self.__class__.__name__}")

    async def disconnect(self):
        if self.connection:
            await self.connection.close()
            print(f"Disconnected from MySQL database {self.__class__.__name__}")


if __name__ == "__main__":
    db = Database()
    asyncio.run(db.connect())
    asyncio.run(db.disconnect())
