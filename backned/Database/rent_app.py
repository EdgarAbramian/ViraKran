import sqlalchemy
from sqlalchemy import select

from backned.Database import Database


class StockDatabase(Database):
    def __init__(self):
        super().__init__()
        self.table = sqlalchemy.Table("rent_app", self.metadata)

    def select(self):
        return self.connection.execute(select(self.table)).fetchall()

    def insert(self, data):
        self.connection.execute(self.table.insert().values(data))
        self.connection.commit()

    def delete(self, id_brand: int):
        self.connection.execute(self.table.delete().where(self.table.c.id == id_brand))
        self.connection.commit()

    def update(self, id_brand: int, data):
        self.connection.execute(self.table.update().where(self.table.c.id == id_brand).values(data))
        self.connection.commit()


if __name__ == "__main__":
    d = StockDatabase()

    print(d.select())
    d.update(4, {"info": "test123"})
    print(d.select())
