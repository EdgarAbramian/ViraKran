from fastapi import APIRouter
from backned.Database import model, brand, stock
import pandas as pd

router = APIRouter(
    prefix="/cran",
    tags=["cran"],
)
modelDB = model.ModelDatabase()
brandDB = brand.BranDatabase()
stockDB = stock.StockDatabase()


@router.get("/stock")
async def get_brand():
    return {"message": pd.DataFrame(stockDB.select()).to_json(orient="records")}


@router.get("/brand")
async def get_brand():
    return {"message": pd.DataFrame(brandDB.select()).to_json(orient="records")}


@router.delete("/brand/delete/{id_brand:int}")
async def del_brand(id_brand: int):
    brandDB.delete(id_brand)
    return {"message": True}


@router.get("/model/{id_brand:int}")
async def get_model(id_brand: int):
    if id_brand:
        response = modelDB.select(id_brand)
    else:
        response = modelDB.select()
    response = pd.DataFrame(response).to_json(orient="records")
    return {"message": response}


@router.get("/model/delete/{id_brand:int}")
async def del_model(id_brand: int):
    modelDB.delete(id_brand)
    return {"message": True}


@router.get("/model/update/{id_brand:int}")
async def get_model(id_brand: int):
    modelDB.update(id_brand, {"model": "test123"})
    return {"message": True}


@router.post("/model/insert")
async def get_model(data: dict):
    modelDB.insert(data)
    return {"message": True}


@router.get("/")
async def root():
    return {"message": "Hello Mother Fucker! This is ViraKran API Cran chapter!"}
