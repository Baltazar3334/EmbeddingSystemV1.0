from loaders.contract_loader import load_contract

from utils.text_cleaning import (
    clean_contract_text
)



from services.match_service import (
    match_contract
)

from llm.worker_reranker import (
    rerank_workers
)

raw = load_contract("default.docx")

cleaned = clean_contract_text(raw)

ranked = match_contract(cleaned)

top_workers = ranked[:10]

reranked = rerank_workers(
    cleaned[:3000],
    top_workers
)

print(reranked)