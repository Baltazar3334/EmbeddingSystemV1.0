from embeddings.embedding_model import embedding_model
from ranking.ranker import rank_workers
from storage.embeddings_store import load_workers_embeddings

"""
Match a contract against cached worker embeddings.
"""

# MATCH CONTRACT =====================================================
def match_contract(contract_text):

    workers = load_workers_embeddings()

    # ERROR HANDLING
    if workers is None:
        raise Exception(
            "No local worker embeddings found. "
            "Please update workers first."
        )

    print("\nGenerating contract embedding...")

    contract_embedding = embedding_model.encode(
        [contract_text]
    )[0]

    ranked = rank_workers(
        contract_embedding,
        workers
    )

    return ranked