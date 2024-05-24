from fastapi import APIRouter

from backend.DataBase.CraneDataBase.BrandDb import BrandDb

from backend.models.DatabaseModels.Models import CraneBrand

router = APIRouter()

brand_db = BrandDb()


@router.post("/select")
async def root(cr: CraneBrand):
    res = await brand_db.select(CraneBrand(**cr.dict(exclude_unset=True)))
    return res


@router.post("/insert")
async def root(cr: CraneBrand):
    res = await brand_db.insert(CraneBrand(**cr.dict(exclude_unset=True)))
    return res


@router.post("/delete")
async def root(cr: CraneBrand):
    res = await brand_db.delete(CraneBrand(**cr.dict(exclude_unset=True)))
    return res


@router.post("/update")
async def root(cr: CraneBrand):
    res = await brand_db.update(CraneBrand(**cr.dict(exclude_unset=True)))
    return res
