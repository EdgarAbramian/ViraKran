from fastapi import APIRouter

from backend.DataBase.UserDatabase.RentalApp import RentalApp

from backend.models.DatabaseModels.Models import RentalApplication

router = APIRouter()

brand_db = RentalApp()


@router.post("/select")
async def root():
    res = await brand_db.select()
    return res


@router.post("/insert")
async def root(values: RentalApplication):
    res = await brand_db.insert(RentalApplication(**values.dict(exclude_unset=True)))
    return res


@router.post("/update")
async def root(email: str, status: bool):
    res = await brand_db.update(email, status)
    return res
