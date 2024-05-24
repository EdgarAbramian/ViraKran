from fastapi import FastAPI
import uvicorn

from routers import CranRouter, UserRouter
from routers.UserRouters import RentalAppRouter

app = FastAPI(
    title="ViraKran",
    description="ViraKran",
    version="1.0.0",
    docs_url="/v1/docs",
)


app.include_router(CranRouter.router, prefix="/Cran")
app.include_router(UserRouter.router, prefix="/User")


@app.get("/")
async def root():
    return {"message": "Hello World"}


if __name__ == "__main__":
    uvicorn.run(app, host="192.168.0.26", port=8001, log_level="info")

