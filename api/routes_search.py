# routes_search.py
from fastapi import APIRouter
from chunker.embedder import embed_chunks
from qdrant.client import get_client
from qdrant.schema import COLLECTION, create_collection
from qdrant_client.models import VectorParams, Distance

router = APIRouter()

@router.get("/query")
def semantic_search(query: str, top_k: int = 5):
    client = get_client()

    # Ensure collection exists
    create_collection()

    query_vec = embed_chunks([query])[0]

    results = client.query_points(
        collection_name=COLLECTION,
        query=query_vec,
        limit=top_k
    )

    # Unpack tuples returned by Qdrant
    matches = [
        {
            "score": score,
            "text": point.payload.get("chunk_text"),
            "doc_id": point.payload.get("doc_id")
        }
        for point, score in results
    ]

    return {
        "query": query,
        "matches": matches
    }
