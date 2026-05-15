"""
FastAPI backend application.
"""

from dotenv import load_dotenv
load_dotenv()

import os
import tempfile

from fastapi import (
    FastAPI,
    UploadFile,
    File,
    Depends
)

from auth.security import verify_token

from services.worker_update_service import (
    update_workers_embeddings
)

from services.match_service import (
    match_contract
)

from loaders.contract_loader import (
    load_contract
)

from utils.text_cleaning import (
    clean_contract_text
)

from config import (
TOP_N_WORKERS,
)

# APP
app = FastAPI()


# ROOT
@app.get("/")
def root():
    return {
        "message": "Embedding System API running"
    }


# UPDATE WORKERS ==========================================
@app.post("/update-workers")
async def update_workers(
    token: str = Depends(verify_token)
):

    count = update_workers_embeddings()

    return {
        "message": "Workers updated",
        "workers": count
    }


# MATCH CONTRACT ==========================================
@app.post("/match-contract")
async def match_contract_api(
    file: UploadFile = File(...),
    token: str = Depends(verify_token)
):

    # TEMP FILE
    suffix = os.path.splitext(file.filename)[1]

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=suffix
    ) as tmp:

        content = await file.read()
        tmp.write(content)

        temp_path = tmp.name

    # LOAD CONTRACT
    raw_contract = load_contract(temp_path)

    contract_text = clean_contract_text(
        raw_contract
    )

    # MATCH
    ranked = match_contract(contract_text)

    return {
        "workers": ranked[:TOP_N_WORKERS]
    }