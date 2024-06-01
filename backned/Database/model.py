import sqlalchemy
from sqlalchemy import select

from backned.Database import Database


class ModelDatabase(Database):
    def __init__(self):
        super().__init__()
        self.table = sqlalchemy.Table("model_cran", self.metadata)

    def select(self, id_brand: int = None):
        if id_brand:
            return self.connection.execute(select(self.table).where(self.table.c.brand_id == id_brand)).fetchall()
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
    d = ModelDatabase()

    print(d.select())
    d.insert({"model": "test1", "brand_id": 4})
    print(d.select())
