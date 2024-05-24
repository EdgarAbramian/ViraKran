import asyncio

from .ModelDb import ModelDb
from .BrandDb import BrandDb
from .CraneStock import CraneStock

__all__ = ['ModelDb', 'BrandDb', 'CraneStock']


class Crane:
    def __init__(self):
        self.model = ModelDb()
        self.brand = BrandDb()
        self.crane_stock = CraneStock()

    async def __aenter__(self):
        await self.model.connect()
        await self.brand.connect()
        await self.crane_stock.connect()

    async def __aexit__(self):
        await self.model.disconnect()
        await self.brand.disconnect()
        await self.crane_stock.disconnect()

# #
# # if __name__ == "__main__":
# #     db = Crane()
# #     res = asyncio.get_event_loop().run_until_complete(db.model.select())
# #     print(res)
