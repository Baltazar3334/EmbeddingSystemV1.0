import os
import tempfile

from typing import Optional

import numpy as np

from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Depends,
    Form
)

from auth.security import verify_token

from services.llm_ranking_service import (
    generate_llm_ranking
)

from storage.rankings_store import (
    load_rankings
)

router = APIRouter()

# GENERATE LLM RANKINGS =============================
@router.post("/generate-llm-ranking")
async def generate_llm_ranking_api(

    contract_id: str = Form(...),

    contract_embedding: Optional[str] = Form(None),

    file: UploadFile = File(None),

    token: str = Depends(verify_token)
):

    temp_path = None


    # FILE PROVIDED
    if file is not None:

        suffix = os.path.splitext(
            file.filename
        )[1]

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=suffix
        ) as tmp:

            content = await file.read()

            tmp.write(content)

            temp_path = tmp.name

    # EMBEDDING PROVIDED
    embedding_array = None

    if (
            contract_embedding is not None
            and contract_embedding != ""
            and contract_embedding != "string"
    ):

        embedding_array = np.array(
            [
                float(x)
                for x in contract_embedding.split(",")
            ]
        )

    # GENERATE RANKING
    result = generate_llm_ranking(

        contract_id=contract_id,

        contract_path=temp_path,

        contract_embedding=embedding_array
    )

    return {

        "message":
            "LLM ranking generated",

        "contract_id":
            contract_id,

        "ranking":
            result
    }

@router.get("/get-ranking/{contract_id}")
def get_ranking(
    contract_id: str,
    token: str = Depends(verify_token)
):

    rankings = load_rankings()

    if contract_id not in rankings:
        return {
            "error": "Ranking not found"
        }

    return rankings[contract_id]