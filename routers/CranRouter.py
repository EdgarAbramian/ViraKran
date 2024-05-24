from fastapi import APIRouter

from routers.CranRouters import BrandRouter, CraneStockRouter, ModelRouter

router = APIRouter()

router.include_router(BrandRouter.router, prefix="/Brand", tags=["Brand"])
router.include_router(ModelRouter.router, prefix="/Model", tags=["Model"])
router.include_router(CraneStockRouter.router, prefix="/Stock", tags=["Stock"])



