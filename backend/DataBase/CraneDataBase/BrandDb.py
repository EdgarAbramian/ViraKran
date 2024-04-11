import asyncio
import pandas as pd

from backend.DataBase.database import Database
from backend.models.DatabaseModels.Models import CraneBrand


# from backend.ViraExceptions.DbExceptions import DbBrandError


class BrandDb(Database):

    def __init__(self):
        super().__init__()
        asyncio.get_event_loop().run_until_complete(super().connect())

    async def select(self, crane_brand: CraneBrand):
        try:
            if crane_brand.brand:
                await self.cursor.execute("SELECT * FROM crane_brand WHERE brand=(%s)", (crane_brand.brand,))
            else:
                await self.cursor.execute("SELECT * FROM crane_brand")
            data = await self.cursor.fetchall()
            data = pd.DataFrame(data, columns=['id', 'name', 'info'])
            return data

        except Exception as e:
            pass

    async def insert(self, crane_brand: CraneBrand):
        try:
            await self.cursor.execute("INSERT INTO crane_brand(brand, info) VALUES (%s, %s)", crane_brand)
            await self.connection.commit()
        except Exception as e:
            await self.connection.rollback()
            print(e)

    async def delete(self, crane_brand: CraneBrand):
        try:
            await self.cursor.execute(
                f"start transaction; set autocommit=0; "
                f"DELETE FROM crane_stock WHERE model_id in"
                f"(select id from crane_model where brand_id in"
                f"(select id from crane_brand where brand = '{crane_brand.brand}'));"
                f"DELETE FROM crane_model WHERE brand_id in (select id from crane_brand where brand = '{crane_brand.brand}'); "
                f"DELETE FROM crane_brand WHERE brand = '{crane_brand.brand}'"
                )
            await self.connection.commit()
        except Exception as e:
            await self.connection.rollback()
            print(e)

    async def update(self, crane_brand: CraneBrand):
        try:
            await self.cursor.execute("UPDATE crane_brand SET info=(%s) WHERE brand=(%s)", crane_brand)
            await self.connection.commit()
        except Exception as e:
            await self.connection.rollback()
            print(e)


if __name__ == "__main__":
    db = BrandDb()
    cr = CraneBrand(brand="tes1t")
    asyncio.get_event_loop().run_until_complete(db.delete(cr))
