from qdrant.client import get_client
from qdrant_client.models import PointStruct
import uuid

def upsert_chunks(chunks, embeddings, doc_id="doc_1"):
    """
    Insert chunks and embeddings into Qdrant collection.
    """
    client = get_client()
    points = []

    for i, (chunk, vector) in enumerate(zip(chunks, embeddings)):
        points.append(
            PointStruct(
                id=str(uuid.uuid4()),  # Valid UUID for each point
                vector=vector,
                payload={
                    "doc_id": doc_id,
                    "chunk_text": chunk,
                    "chunk_id": i
                }
            )
        )

    client.upsert(collection_name="doc_chunks", points=points)
