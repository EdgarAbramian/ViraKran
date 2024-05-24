from fastapi import APIRouter

from backend.DataBase.UserDatabase.LoginData import UserLoginData

from backend.models.DatabaseModels.Models import CraneBrand, SelectUser, UserLoginForm, UpdtUser

router = APIRouter()

brand_db = UserLoginData()


@router.post("/select")
async def root(user: SelectUser):
    res = await brand_db.select(SelectUser(**user.dict(exclude_unset=True)))
    return res


@router.post("/insert")
async def root(values: UserLoginForm):
    res = await brand_db.insert(UserLoginForm(**values.dict(exclude_unset=True)))
    return res


@router.post("/delete")
async def root(username: str):
    res = await brand_db.delete(username)
    return res


@router.post("/update")
async def root(username: UpdtUser):
    res = await brand_db.update(UpdtUser(**username.dict(exclude_unset=True)))
    return res
