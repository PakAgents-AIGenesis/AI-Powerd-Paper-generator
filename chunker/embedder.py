import numpy as np

# Set embedding dimension to match Qdrant collection
EMBED_DIM = 384  # Must match the dimension used in create_collection()

# Dummy model for testing without sentence-transformers
class DummyModel:
    def encode(self, chunks):
        """
        Return a random vector for each chunk.
        Each vector has EMBED_DIM floats.
        """
        return [np.random.rand(EMBED_DIM).tolist() for _ in chunks]

# Use dummy model
model = DummyModel()

def embed_chunks(chunks):
    """
    Generate vector embeddings for a list of text chunks.
    Works without the sentence-transformers package.
    """
    embeddings = model.encode(chunks)
    return embeddings
