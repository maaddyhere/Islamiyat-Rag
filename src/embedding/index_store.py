# src/embeddings/index_store.py
import json
import faiss

def load_documents(path="data/processed/cleaned_chunks.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def build_and_save_index(embeddings, path: str) -> None:
    """Build a FAISS index for normalized embeddings and save it to disk."""
    if embeddings.ndim != 2:
        raise ValueError("Embeddings must be a 2D array")

    dim = embeddings.shape[1]
    index = faiss.IndexFlatIP(dim)
    index.add(embeddings)
    faiss.write_index(index, path)


# Each doc already has: text, chapter, lesson, section_type, chunk_id