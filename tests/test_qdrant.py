from chunker.chunker import split_text_to_chunks
from chunker.embedder import embed_chunks
from qdrant.indexer import upsert_chunks
from qdrant.schema import create_collection
from qdrant.client import get_client

# 1️⃣ Sample text
text = """This is the first paragraph of the document.

This is the second paragraph. It contains more information for testing.
"""

# 2️⃣ Split text into chunks
chunks = split_text_to_chunks(text)
print("Chunks:", chunks)

# 3️⃣ Generate embeddings
embeddings = embed_chunks(chunks)
print("Number of embeddings:", len(embeddings))

# 4️⃣ Create Qdrant collection
create_collection()

# 5️⃣ Upsert chunks into Qdrant
upsert_chunks(chunks, embeddings, doc_id="doc_test")

# 6️⃣ Test search
client = get_client()
result = client.search(
    collection_name="doc_chunks",
    query_vector=embeddings[0],
    limit=1
)

print("Top result:", result[0].payload["chunk_text"])
