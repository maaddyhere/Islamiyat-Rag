"""
Run this script ONCE to process the PDF and build the FAISS index.
    python scripts/build_index.py
"""
import json
from src.config.settings import METADATA_PATH, FAISS_INDEX_PATH, INDEX_DIR, PROCESSED_DIR
from src.ingestion.pdf_extractor import extract_text, build_documents
from src.ingestion.cleaner import clean_documents
from src.ingestion.chunker import split_documents
from src.embeddings.encoder import encode_texts
from src.embeddings.index_store import build_and_save_index

def main():
    print("Step 1/4 — Extracting PDF...")
    raw_docs = build_documents(extract_text())

    print("Step 2/4 — Cleaning & chunking...")
    docs = clean_documents(raw_docs)
    chunks = split_documents(docs)
    print(f"Step 3/4 — Encoding {len(chunks)} chunks...")
    texts = [c.page_content for c in chunks]
    embeddings = encode_texts(texts)

    print("Step 4/4 — Saving index & metadata...")
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    INDEX_DIR.mkdir(parents=True, exist_ok=True)
    build_and_save_index(embeddings, str(FAISS_INDEX_PATH))

    metadata = [
        {"text": c.page_content, "source": c.metadata.get("source", ""),
         "page": c.metadata.get("page"), "section_type": c.metadata.get("section_type", ""),
         "chunk_index": c.metadata.get("chunk_index")}
        for c in chunks
    ]
    with open(METADATA_PATH, "w", encoding="utf-8") as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)
    print(f"Done. {len(chunks)} chunks indexed.")

if __name__ == "__main__":
    main()