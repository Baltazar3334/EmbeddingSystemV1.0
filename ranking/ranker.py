import numpy as np

from config import (
    KEYWORD_WEIGHT,
    BIO_WEIGHT
)

"""
Rank workers against a contract embedding
using keyword and bio similarity scores.
"""

# RANK WORKERS =====================================================
def rank_workers(contract_embedding, workers):

    ranked = []

    print(f"\nRanking {len(workers)} workers...")

    for worker in workers:

        keyword_score = np.dot(
            contract_embedding,
            worker["keyword_embedding"]
        )

        bio_score = np.dot(
            contract_embedding,
            worker["bio_embedding"]
        )

        # WEIGHTED SCORE FUSION
        final_score = (
                KEYWORD_WEIGHT * keyword_score
                +
                BIO_WEIGHT * bio_score
        )

        ranked.append({
            "id": worker["id"],
            "name": worker["name"],

            "score":
                round(float(final_score), 4),

            "keyword_score":
                round(float(keyword_score), 4),

            "bio_score":
                round(float(bio_score), 4),

            "keywords": worker["keywords"]
        })

    ranked.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return ranked