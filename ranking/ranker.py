"""
Worker ranking system.
"""

import numpy as np

from sklearn.metrics.pairwise import (
    cosine_similarity
)


# RANK WORKERS ============================
def rank_workers(contract_embedding, workers):

    ranked = []

    print(f"\nRanking {len(workers)} workers...")

    for worker in workers:


        # KEYWORD MATCHING=====================

        keyword_scores = []

        for keyword_embedding in worker[
            "keyword_embeddings"
        ]:

            sim = cosine_similarity(
                [contract_embedding],
                [keyword_embedding]
            )[0][0]

            keyword_scores.append(sim)

        # BEST KEYWORD MATCH
        keyword_score = max(keyword_scores)


        # BIO MATCHING =============================

        bio_score = cosine_similarity(
            [contract_embedding],
            [worker["bio_embedding"]]
        )[0][0]


        ranked.append({

            "id": worker["id"],
            "name": worker["name"],

            "keyword_score":
                round(float(keyword_score), 4),

            "bio_score":
                round(float(bio_score), 4),

            "semantic_score":
                (round(float(bio_score), 4) + round(float(keyword_score), 4)) * 0.5,

            "keywords": worker["keywords"]
        })

    ranked.sort(
        key=lambda x: (
                x["keyword_score"] +
                x["bio_score"]
        ),
        reverse=True
    )

    return ranked