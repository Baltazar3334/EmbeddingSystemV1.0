from fastapi import (
    APIRouter,
    UploadFile,
    File
)

import tempfile
import shutil
import os

from fastapi import APIRouter
from pydantic import BaseModel

from services.worker_update_service import (
    update_workers_embeddings
)

from services.match_service import (
    match_contract
)

from utils.text_cleaning import (
    clean_contract_text
)

"""
API routes for worker matching system.
"""

router = APIRouter()


# REQUEST MODEL =====================================================

class MatchRequest(BaseModel):
    contract_text: str


# UPDATE WORKERS =====================================================

@router.post("/update-workers")
def update_workers():

    count = update_workers_embeddings()

    return {
        "status": "success",
        "workers_updated": count
    }


# MATCH CONTRACT =====================================================

@router.post("/match")
def match_workers(request: MatchRequest):

    contract_text = clean_contract_text(
        request.contract_text
    )

    ranked = match_contract(contract_text)

    return {
        "status": "success",
        "results": ranked[:20]
    }

@router.post("/match-file")
def match_file(file: UploadFile = File(...)):

    # TEMP FILE
    suffix = os.path.splitext(file.filename)[1]

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=suffix
    ) as temp_file:

        shutil.copyfileobj(
            file.file,
            temp_file
        )

        temp_path = temp_file.name

    try:

        # LOAD CONTRACT
        from loaders.contract_loader import (
            load_contract
        )

        raw_contract = load_contract(temp_path)

        contract_text = clean_contract_text(
            raw_contract
        )

        ranked = match_contract(contract_text)

        return {
            "status": "success",
            "filename": file.filename,
            "results": ranked[:20]
        }

    finally:

        # DELETE TEMP FILE
        os.remove(temp_path)