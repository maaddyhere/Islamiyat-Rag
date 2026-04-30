import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from src.config.settings import EMBEDDING_MODEL

# Module-level singleton — loaded once, reused everywhere
_model: SentenceTransformer | None = None

def get_model() -> SentenceTransformer:
    global _model
    if _model is None:
        _model = SentenceTransformer(EMBEDDING_MODEL)
    return _model

def encode_texts(texts: list[str]) -> np.ndarray:
    vecs = get_model().encode(texts, show_progress_bar=True, batch_size=64)
    faiss.normalize_L2(vecs)          # normalize for cosine similarity
    return vecs.astype("float32")

def embed_query(query: str) -> np.ndarray:
    if not query.strip():
        raise ValueError("Query must not be empty")
    vec = get_model().encode(query, convert_to_numpy=True)
    vec = vec.reshape(1, -1).astype("float32")
    faiss.normalize_L2(vec)
    return vec