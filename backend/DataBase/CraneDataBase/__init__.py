import asyncio

from ModelDb import ModelDb
from BrandDb import BrandDb
from ModelInfoDb import ModelInfoDb
from CraneStock import CraneStock

__all__ = ['ModelDb', 'BrandDb', 'ModelInfoDb', 'CraneStock']


class Crane(object):
    def __init__(self):
        self.model = ModelDb()
        self.brand = BrandDb()
        self.model_info = ModelInfoDb()
        self.crane_stock = CraneStock()

    async def __aenter__(self):
        await self.model.connect()
        await self.brand.connect()
        await self.model_info.connect()
        await self.crane_stock.connect()

    async def __aexit__(self):
        await self.model.disconnect()
        await self.brand.disconnect()
        await self.model_info.disconnect()
        await self.crane_stock.disconnect()


if __name__ == "__main__":
    db = Crane()
    res = asyncio.get_event_loop().run_until_complete(db.model.select())
    print(res)
