from fastapi import APIRouter

from backend.DataBase.CraneDataBase.CraneStock import CraneStock

from backend.models.DatabaseModels.Models import CranStockModel

router = APIRouter()

stock_db = CraneStock()


@router.post("/select")
async def root(cr: CranStockModel):
    res = await stock_db.select(CranStockModel(**cr.dict(exclude_unset=True)))
    return res


@router.post("/insert")
async def root(cr: CranStockModel):
    res = await stock_db.insert(CranStockModel(**cr.dict(exclude_unset=True)))
    return res


@router.post("/delete")
async def root(cr: CranStockModel):
    res = await stock_db.delete(CranStockModel(**cr.dict(exclude_unset=True)))
    return res


@router.post("/update")
async def root(cr: CranStockModel):
    res = await stock_db.update(CranStockModel(**cr.dict(exclude_unset=True)))
    return res
