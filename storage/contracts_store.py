"""
Contract embeddings storage.
"""

import json
import os

import numpy as np


CONTRACTS_PATH = "contracts_embeddings.json"


# LOAD ====================================================
def load_contracts(path=CONTRACTS_PATH):

    if not os.path.exists(path):
        return {}

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    for contract_id in data:

        data[contract_id]["embedding"] = np.array(
            data[contract_id]["embedding"]
        )

    return data


# SAVE ====================================================
def save_contract(
    contract_id,
    cleaned_text,
    embedding,
    path=CONTRACTS_PATH
):

    data = load_contracts(path)

    data[contract_id] = {
        "cleaned_text": cleaned_text,
        "embedding": embedding.tolist()
    }

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)