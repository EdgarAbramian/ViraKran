from fastapi import APIRouter

from backend.DataBase.CraneDataBase.ModelDb import ModelDb

from backend.models.DatabaseModels.Models import CraneModelSelect,CraneModel, CraneModelDelete, CraneModelUpdate, CraneBrand

router = APIRouter()

model_db = ModelDb()


@router.post("/select")
async def root(cr: CraneModelSelect):
    res = await model_db.select(CraneModelSelect(**cr.dict(exclude_unset=True)))
    return res


@router.post("/insert")
async def root(cr: CraneModel):
    res = await model_db.insert(CraneModel(**cr.dict(exclude_unset=True)))
    return res


@router.post("/delete")
async def root(cr: CraneModelDelete):
    res = await model_db.delete(CraneModelDelete(**cr.dict(exclude_unset=True)))
    return res


@router.post("/update")
async def root(cr: CraneModelUpdate):
    res = await model_db.update(CraneModelUpdate(**cr.dict(exclude_unset=True)))
    return res
