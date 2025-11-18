# services/embeddings_qdrant.py
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
import numpy as np
import os

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    print("❌ google-generativeai not available, using fallback embeddings")

try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False
    print("❌ scikit-learn not available, using random embeddings")

class GeminiEmbedder:
    def __init__(self, api_key=None):
        # FIX: Use environment variable or provided key
        self.api_key = api_key or os.getenv('GOOGLE_API_KEY')
        print(f"🔑 Embedder API Key: {'***' + self.api_key[-4:] if self.api_key else 'NOT SET'}")
        
        if not self.api_key:
            print("❌ No API key for Gemini embeddings, using fallback")
            self.available = False
            return
            
        if not GEMINI_AVAILABLE:
            print("❌ google-generativeai not installed, using fallback")
            self.available = False
            return

        try:
            genai.configure(api_key=self.api_key)
            self.available = True
            print("✅ Gemini Embedder configured successfully")
        except Exception as e:
            print(f"❌ Error configuring Gemini Embedder: {e}")
            self.available = False

    def get_embedding(self, text):
        """Get embedding using Gemini API or fallback"""
        if self.available:
            try:
                print(f"🔄 Getting Gemini embedding for {len(text)} chars...")
                result = genai.embed_content(
                    model="models/embedding-001",
                    content=text,
                    task_type="retrieval_document"
                )
                print("✅ Gemini embedding successful")
                return result['embedding']
            except Exception as e:
                print(f"❌ Gemini embedding failed: {e}")
        
        # Fallback to TF-IDF
        return self.get_tfidf_embedding(text)

    def get_tfidf_embedding(self, text):
        """Fallback TF-IDF embedding"""
        if not SKLEARN_AVAILABLE:
            print("🔄 Using random embedding (scikit-learn not available)")
            return np.random.rand(512).tolist()
            
        try:
            # Use a simple TF-IDF approach
            from sklearn.feature_extraction.text import TfidfVectorizer
            import numpy as np
            
            # Create vectorizer with limited features for efficiency
            vectorizer = TfidfVectorizer(max_features=512, stop_words='english')
            
            # Fit and transform the text
            embedding = vectorizer.fit_transform([text]).toarray()[0]
            
            # Pad or truncate to 512 dimensions
            if len(embedding) < 512:
                embedding = np.pad(embedding, (0, 512 - len(embedding)))
            else:
                embedding = embedding[:512]
                
            print("✅ TF-IDF embedding generated")
            return embedding.tolist()
        except Exception as e:
            print(f"❌ TF-IDF embedding failed: {e}")
            return np.random.rand(512).tolist()

class VectorMemory:
    def __init__(self, qdrant_url=":memory:", collection_name="exam_chunks", api_key=None):
        print(f"🔄 Initializing VectorMemory with Qdrant: {qdrant_url}")
        
        try:
            self.client = QdrantClient(url=qdrant_url)
            self.collection = collection_name
            self.embedder = GeminiEmbedder(api_key)

            # Create collection if it doesn't exist
            try:
                self.client.get_collection(collection_name)
                print(f"✅ Collection '{collection_name}' exists")
            except Exception:
                self.client.create_collection(
                    collection_name=collection_name,
                    vectors_config=VectorParams(size=512, distance=Distance.COSINE)
                )
                print(f"✅ Created collection '{collection_name}'")
                
        except Exception as e:
            print(f"❌ Qdrant initialization failed: {e}")
            print("🔄 Using fallback memory storage")
            self.client = None
            self._fallback_storage = []

    def store_document(self, chunks, metadata):
        """Store document chunks in vector database"""
        if self.client is None:
            # Fallback storage
            print(f"💾 Storing {len(chunks)} chunks in fallback storage")
            for i, chunk in enumerate(chunks):
                self._fallback_storage.append({
                    "text": chunk,
                    "metadata": {**metadata, "chunk_id": i}
                })
            return

        try:
            print(f"🔄 Generating embeddings for {len(chunks)} chunks...")
            vectors = [self.embedder.get_embedding(chunk) for chunk in chunks]

            points = []
            for idx, (vec, chunk) in enumerate(zip(vectors, chunks)):
                points.append(
                    PointStruct(
                        id=idx,
                        vector=vec,
                        payload={"text": chunk, **metadata, "chunk_id": idx}
                    )
                )

            self.client.upsert(
                collection_name=self.collection,
                points=points
            )
            print(f"✅ Stored {len(chunks)} chunks in Qdrant database")
        except Exception as e:
            print(f"❌ Failed to store in Qdrant: {e}")
            # Fallback to simple storage
            self._fallback_storage = []
            for i, chunk in enumerate(chunks):
                self._fallback_storage.append({
                    "text": chunk,
                    "metadata": {**metadata, "chunk_id": i}
                })

    def retrieve(self, query, top_k=5):
        """Retrieve relevant chunks for query"""
        if self.client is None:
            # Fallback retrieval - return first N chunks
            print(f"🔍 Fallback retrieval: returning first {top_k} chunks")
            return self._fallback_storage[:top_k] if hasattr(self, '_fallback_storage') else []

        try:
            print(f"🔍 Retrieving top {top_k} chunks for query: '{query}'")
            embedded_query = self.embedder.get_embedding(query)

            results = self.client.search(
                collection_name=self.collection,
                query_vector=embedded_query,
                limit=top_k
            )

            print(f"✅ Retrieved {len(results)} chunks from Qdrant")
            return [r.payload for r in results]
        except Exception as e:
            print(f"❌ Qdrant retrieval failed: {e}")
            # Fallback: return first N chunks
            return self._fallback_storage[:top_k] if hasattr(self, '_fallback_storage') else []