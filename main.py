from fastapi import FastAPI
import uvicorn
from backned.Routers import cran

app = FastAPI(
    title="ViraKran",
    description="ViraKran",
    version="1.0.0",
    docs_url="/docs",
)

app.include_router(cran.router)


@app.get("/")
async def root():
    return {"message": "Hello Mother Fucker! This is ViraKran API!"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001, log_level="info")
