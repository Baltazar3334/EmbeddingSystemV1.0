from embeddings.embedding_model import embedding_model

"""
Generate keyword and bio embeddings for workers.
"""

# GENERATE WORKER EMBEDDINGS =========================================
def generate_worker_embeddings(workers):

    print("\nGenerating worker embeddings...")

    for worker in workers:

        keywords = worker.get("keywords", [])
        bio = worker.get("bio", "")

        keywords_text = " ".join(keywords)

        # KEYWORD EMBEDDING
        worker["keyword_embedding"] = embedding_model.encode(
            [keywords_text]
        )[0]

        # BIO EMBEDDING
        worker["bio_embedding"] = embedding_model.encode(
            [bio]
        )[0]

    print("Worker embeddings generated")

    return workers