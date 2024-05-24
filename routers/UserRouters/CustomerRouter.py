from fastapi import APIRouter

from backend.DataBase.CustomersList.CustListDb import CustListDb

from backend.models.DatabaseModels.Models import MailingList

router = APIRouter()

brand_db = CustListDb()


@router.post("/select")
async def root():
    res = await brand_db.select()
    return res


@router.post("/insert")
async def root(values: MailingList):
    res = await brand_db.insert(MailingList(**values.dict(exclude_unset=True)))
    return res


@router.post("/delete")
async def root(email: str):
    res = await brand_db.delete(email)
    return res
