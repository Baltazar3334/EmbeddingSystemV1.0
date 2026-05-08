from loaders.worker_loader import load_workers_from_api
from embeddings.worker_embeddings import generate_worker_embeddings
from storage.embeddings_store import save_workers_embeddings

from config import API_URL

"""
Update and cache worker embeddings from the API.
"""

# UPDATE WORKERS =====================================================
def update_workers_embeddings():

    print("\nUpdating workers embeddings...")

    workers = load_workers_from_api(API_URL)

    workers = generate_worker_embeddings(workers)

    save_workers_embeddings(workers)

    print("\nWorkers embeddings updated")

    return len(workers)