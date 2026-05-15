# SAVE =====================================================
import json
import os

import numpy as np
from config import EMBEDDINGS_CACHE_PATH

"""
Save and load worker embeddings cache.
"""

def save_workers_embeddings(workers, path=EMBEDDINGS_CACHE_PATH):

    serializable_workers = []

    for worker in workers:
        serializable_workers.append({
            "id": worker["id"],
            "name": worker["name"],
            "keywords": worker["keywords"],
            "bio": worker["bio"],

            "keyword_embeddings": [
                emb.tolist()
                for emb in worker["keyword_embeddings"]
            ],

            "bio_embedding":
                worker["bio_embedding"].tolist()
        })

    with open(path, "w", encoding="utf-8") as f:
        json.dump(
            serializable_workers,
            f,
            ensure_ascii=False
        )

    print(f"\nSaved embeddings to {path}")


# LOAD =====================================================
def load_workers_embeddings(path=EMBEDDINGS_CACHE_PATH):

    if not os.path.exists(path):
        return None

    with open(path, "r", encoding="utf-8") as f:
        workers = json.load(f)

    for worker in workers:
        worker["keyword_embeddings"] = [
            np.array(emb)
            for emb in worker["keyword_embeddings"]
        ]

        worker["bio_embedding"] = np.array(
            worker["bio_embedding"]
        )

    print(f"\nLoaded cached embeddings from {path}")

    return workers