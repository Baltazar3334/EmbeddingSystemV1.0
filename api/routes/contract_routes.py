import os
import tempfile

from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Depends
)

from auth.security import verify_token

from services.match_service import (
    match_contract
)

from services.contract_embedding_service import (
    generate_contract_embedding
)

from loaders.contract_loader import (
    load_contract
)

from utils.text_cleaning import (
    clean_contract_text
)

from config import TOP_N_WORKERS

router = APIRouter()

# GENERATE CONTRACT EMBEDDING =========================
@router.post("/generate-contract-embedding")
async def generate_contract_embedding_api(
    contract_id: str,
    file: UploadFile = File(...),
    token: str = Depends(verify_token)
):

    suffix = os.path.splitext(file.filename)[1]

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=suffix
    ) as tmp:

        content = await file.read()
        tmp.write(content)

        temp_path = tmp.name

    result = generate_contract_embedding(
        contract_id,
        temp_path
    )

    return result


# MATCH CONTRACT ==========================================
@router.post("/match-contract")
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
        "workers": ranked
    }