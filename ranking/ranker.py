from sklearn.metrics.pairwise import cosine_similarity


# RANK WORKERS =====================================================
def rank_workers(contract_embedding, workers):

    ranked = []

    print(f"\nRanking {len(workers)} workers...")

    for worker in workers:

        keyword_score = cosine_similarity(
            [contract_embedding],
            [worker["keyword_embedding"]]
        )[0][0]

        bio_score = cosine_similarity(
            [contract_embedding],
            [worker["bio_embedding"]]
        )[0][0]

        # WEIGHTED SCORE FUSION
        final_score = (
            0.8 * keyword_score
            +
            0.2 * bio_score
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