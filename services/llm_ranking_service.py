"""
LLM ranking generation service.
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
    load_contracts,
    save_contract
)

from storage.embeddings_store import (
    load_workers_embeddings
)

from ranking.ranker import (
    rank_workers
)

from llm.worker_evaluator import (
    evaluate_worker
)

from storage.rankings_store import (
    save_ranking
)

from config import (
KEYWORD_WEIGHT,
BIO_WEIGHT,
LLM_WEIGHT
)

# GENERATE LLM RANKING ===================================
def generate_llm_ranking(

    contract_id,

    contract_path=None,

    contract_embedding=None
):

    print(
        f"\nGenerating LLM ranking "
        f"for contract: {contract_id}"
    )

    contracts = load_contracts()


    # CASE 1 PROVIDED EMBEDDING =========================
    if contract_embedding is not None:

        print("Using provided contract embedding")

        embedding = contract_embedding

        cleaned_text = ""


    # CASE 2 PROVIDED CONTRACT FILE =====================
    elif contract_path is not None:

        print(
            "Generating embedding "
            "from contract file"
        )

        raw = load_contract(contract_path)

        cleaned_text = clean_contract_text(raw)

        embedding = embedding_model.encode(
            [cleaned_text]
        )[0]

        # SAVE LOCAL CACHE
        save_contract(
            contract_id,
            cleaned_text,
            embedding
        )


    # CASE 3 LOAD LOCAL CACHE =======================
    else:

        print("Trying local contract cache")

        if contract_id not in contracts:

            raise Exception(
                "Contract embedding not found"
            )

        cached = contracts[contract_id]

        embedding = cached["embedding"]

        cleaned_text = cached[
            "cleaned_text"
        ]


    # LOAD WORKERS =======================================
    workers = load_workers_embeddings()

    if workers is None:
        raise Exception(
            "No worker embeddings found"
        )


    # EMBEDDING RETRIEVAL ================================
    ranked = rank_workers(
        embedding,
        workers
    )

    top_workers = ranked[:100]


    # LLM RERANKING ======================================
    final_workers = []

    for worker in top_workers:
        llm_data = evaluate_worker(

            cleaned_text,

            worker
        )

        worker["llm_score"] = (
            llm_data["llm_score"]
        )

        worker["llm_reason"] = (
            llm_data["reason"]
        )

        # FINAL HYBRID SCORE
        worker["final_score"] = round(

            (
                    KEYWORD_WEIGHT * worker["keyword_score"]
                    +
                    BIO_WEIGHT * worker["bio_score"]
                    +
                    LLM_WEIGHT * (
                            worker["llm_score"] / 100
                    )
            ),

            4
        )

        final_workers.append(worker)

    # SORT FINAL RESULTS
    final_workers.sort(

        key=lambda x: x["final_score"],

        reverse=True
    )


    # SAVE RANKING =======================================
    save_ranking(
        contract_id,
        final_workers
    )

    print("LLM ranking generated")

    return final_workers