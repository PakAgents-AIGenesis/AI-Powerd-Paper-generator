# schema.py
from qdrant.client import get_client
from qdrant_client.models import VectorParams, Distance

# === Constants used in all Qdrant operations ===
COLLECTION = "doc_chunks"
VECTOR_SIZE = 384
DISTANCE = Distance.COSINE  # use Qdrant Distance object

def create_collection():
    """Create Qdrant collection if not exists"""
    client = get_client()
    collections = [c.name for c in client.get_collections().collections]
    if COLLECTION not in collections:
        client.recreate_collection(
            collection_name=COLLECTION,
            vectors_config=VectorParams(size=VECTOR_SIZE, distance=DISTANCE)
        )
        print(f"Collection '{COLLECTION}' created.")
    else:
        print(f"Collection '{COLLECTION}' already exists.")
