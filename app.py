"""
FastAPI backend application.
"""

from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI

from api.routes.worker_routes import router as worker_router
from api.routes.contract_routes import router as contract_router
from api.routes.ranking_routes import router as ranking_router


# APP ====================================================
app = FastAPI()


# ROOT ===================================================
@app.get("/")
def root():
    return {
        "message": "Embedding System API running"
    }


# ROUTERS ================================================
app.include_router(worker_router)
app.include_router(contract_router)
app.include_router(ranking_router)