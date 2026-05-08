from fastapi import FastAPI

from api.routes import router


app = FastAPI(
    title="Worker Matching API",
    version="1.0"
)

app.include_router(router)