import sys

from config import (
    API_URL,
    DEFAULT_CONTRACT,
    TOP_N_WORKERS
)

from loaders.contract_loader import load_contract
from loaders.worker_loader import load_workers_from_api

from utils.text_cleaning import clean_contract_text

from embeddings.worker_embeddings import generate_worker_embeddings

from embeddings.embedding_model import embedding_model

from storage.embeddings_store import (
    save_workers_embeddings,
    load_workers_embeddings
)

from ranking.ranker import rank_workers


# MAIN =====================================================
if __name__ == "__main__":

    # CONTRACT =========================================
    if len(sys.argv) > 1:
        contract_path = sys.argv[1]
    else:
        contract_path = DEFAULT_CONTRACT

    print(f"\nUsing contract file: {contract_path}")

    raw_contract = load_contract(contract_path)

    contract_text = clean_contract_text(raw_contract)

    # WORKERS TRY CACHE FIRST ======================
    workers = load_workers_embeddings()
    # CACHE MISS
    if workers is None:
        workers = load_workers_from_api(API_URL)

        workers = generate_worker_embeddings(workers)

        save_workers_embeddings(workers)

    contract_embedding = embedding_model.encode(
        [contract_text]
    )[0]

    # RANKING =========================================
    ranked = rank_workers(
        contract_embedding,
        workers
    )

    # OUTPUT =========================================
    print(f"\nTOP {TOP_N_WORKERS} WORKERS:")

    for r in ranked[:TOP_N_WORKERS]:

        print(
            f"\n{r['name']} "
            f"| final: {r['score']} "
            f"| kw: {r['keyword_score']} "
            f"| bio: {r['bio_score']}"
        )

        print("Keywords:")

        for kw in r["keywords"][:3]:
            print(f" - {kw}")