from qdrant_client import QdrantClient

# In-memory Qdrant (no Docker needed)
client = QdrantClient(":memory:")

def get_client():
    return client
