from sentence_transformers import SentenceTransformer

from config import MODEL_NAME


embedding_model = SentenceTransformer(MODEL_NAME)