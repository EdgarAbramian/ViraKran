from fastapi import APIRouter

from routers.UserRouters import loginRouter, RentalAppRouter, CustomerRouter

router = APIRouter()

router.include_router(loginRouter.router, prefix="/Login", tags=["User"])
router.include_router(RentalAppRouter.router, prefix="/RentalApp", tags=["RentalApp"])
router.include_router(CustomerRouter.router, prefix="/Customers", tags=["Customers"])



