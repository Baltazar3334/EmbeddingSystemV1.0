"""
Generate worker embeddings.
"""

from embeddings.embedding_model import (
    embedding_model
)


# GENERATE WORKER EMBEDDINGS ===============================
def generate_worker_embeddings(workers):

    print("\nGenerating worker embeddings...")

    for worker in workers:

        keywords = worker.get("keywords", [])
        bio = worker.get("bio", "")

        # KEYWORD EMBEDDINGS
        worker["keyword_embeddings"] = (
            embedding_model.encode(keywords)
        )

        # BIO EMBEDDING
        worker["bio_embedding"] = (
            embedding_model.encode([bio])[0]
        )

    print("Worker embeddings generated")

    return workers