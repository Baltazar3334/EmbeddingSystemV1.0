API_URL = "https://profiles.pioneer.uniza.sk/api/researchers?api_key=fXdert5kcdf8s7hflbmns8d7dlvkskHG2uRtRF345jGj"

MODEL_NAME = "all-MiniLM-L6-v2"

#contract to be used when none is sent in a request for testing
DEFAULT_CONTRACT = "default.docx"

EMBEDDINGS_CACHE_PATH = "workers_embeddings.json"

#amount of workers to send back ranked from best to worst similarity
TOP_N_WORKERS = 20

#how much similarity does a worker need to have to be considered
SIMILARITY_THRESHOLD = 0.3 #not implemented


#weights of various components of the worker ratings

KEYWORD_WEIGHT = 0.4

BIO_WEIGHT = 0.3

LLM_WEIGHT = 0.3