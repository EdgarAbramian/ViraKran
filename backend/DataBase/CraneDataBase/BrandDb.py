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
        """
        Selects data from the crane_brand table based on the brand provided in the CraneBrand object.

        Args:
            crane_brand (CraneBrand): An object containing the brand information for data selection.

        Returns:
            pd.DataFrame: A DataFrame containing the selected data with columns ['id', 'name', 'info'].
        """
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
        """
        Inserts a new crane brand into the database.

        Args:
            crane_brand (CraneBrand): The CraneBrand object to insert.

        Returns:
            None
        """
        try:
            # Execute the SQL query to insert the crane brand into the database
            await self.cursor.execute("INSERT INTO crane_brand(brand, info) VALUES (%s, %s)", crane_brand)

            # Commit the transaction
            await self.connection.commit()
        except Exception as e:
            # Rollback the transaction in case of an error
            await self.connection.rollback()
            print(e)

    async def delete(self, crane_brand: CraneBrand):
        """
        Delete records related to the given crane brand from the database.

        Args:
            crane_brand (CraneBrand): The crane brand object to be deleted.

        Returns:
            None
        """

        try:
            # Start a transaction and disable autocommit
            await self.cursor.execute(
                f"start transaction; set autocommit=0; "
                f"DELETE FROM crane_stock WHERE model_id in "
                f"(select id from crane_model where brand_id in "
                f"(select id from crane_brand where brand = '{crane_brand.brand}')); "
                f"DELETE FROM crane_model WHERE brand_id in (select id from crane_brand where brand = '{crane_brand.brand}'); "
                f"DELETE FROM crane_brand WHERE brand = '{crane_brand.brand}'"
            )
            await self.connection.commit()
        except Exception as e:
            # Rollback the transaction in case of an exception
            await self.connection.rollback()
            print(e)

    async def update(self, crane_brand: CraneBrand):
        """
        Update the information of a crane brand in the database.

        Args:
            crane_brand (CraneBrand): The CraneBrand object containing the information to update.

        Raises:
            Exception: If an error occurs during the update process.
        """
        try:
            # Execute the SQL update query with the crane_brand information
            await self.cursor.execute("UPDATE crane_brand SET info=(%s) WHERE brand=(%s)", crane_brand)

            # Commit the transaction
            await self.connection.commit()
        except Exception as e:
            # Rollback the transaction if an error occurs
            await self.connection.rollback()
            print(e)


if __name__ == "__main__":
    db = BrandDb()
    cr = CraneBrand(brand="tes1t")
    asyncio.get_event_loop().run_until_complete(db.delete(cr))
