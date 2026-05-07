import json
from pathlib import Path

import faiss

from src.config.settings import FAISS_INDEX_PATH, METADATA_PATH, TOP_K
from src.embedding.encoder import embed_query

_index = None
_docs = None


def load_docs(path: Path = METADATA_PATH) -> list[dict]:
    global _docs
    if _docs is None:
        with open(path, "r", encoding="utf-8") as f:
            _docs = json.load(f)
    return _docs


def load_index(path: Path = FAISS_INDEX_PATH):
    global _index
    if _index is None:
        path = Path(path)
        if not path.exists():
            raise FileNotFoundError(f"FAISS index not found: {path}")
        _index = faiss.read_index(str(path))
    return _index


def search(query: str, k: int = TOP_K) -> list[dict]:
    if not query.strip():
        return []

    index = load_index()
    docs = load_docs()
    q_vec = embed_query(query)

    if q_vec.shape[1] != index.d:
        raise ValueError(
            f"Query vector dimension ({q_vec.shape[1]}) does not match index dimension ({index.d})"
        )

    distances, ids = index.search(q_vec, k)
    results: list[dict] = []
    for idx, score in zip(ids[0], distances[0]):
        if idx < 0 or idx >= len(docs):
            continue
        doc = docs[idx].copy()
        doc["score"] = float(score)
        results.append(doc)

    return results
