from fastapi import APIRouter, Depends

from auth.security import verify_token

from services.worker_update_service import (
    update_workers_embeddings
)

router = APIRouter()


# UPDATE WORKERS ==========================================
@router.post("/update-workers")
async def update_workers(
    token: str = Depends(verify_token)
):

    count = update_workers_embeddings()

    return {
        "message": "Workers updated",
        "workers": count
    }