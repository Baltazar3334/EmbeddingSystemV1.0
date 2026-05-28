"""
Contract embedding generation service.
"""

from embeddings.embedding_model import (
    embedding_model
)

from loaders.contract_loader import (
    load_contract
)

from utils.text_cleaning import (
    clean_contract_text
)

from storage.contracts_store import (
    save_contract
)


# GENERATE CONTRACT EMBEDDING =============================
def generate_contract_embedding(
    contract_id,
    contract_path
):

    raw = load_contract(contract_path)

    cleaned = clean_contract_text(raw)

    embedding = embedding_model.encode(
        [cleaned]
    )[0]

    save_contract(
        contract_id,
        cleaned,
        embedding
    )

    return {
        "contract_id": contract_id,
        "cleaned_text": cleaned
    }