"""
scripts/build_index.py

Run this ONCE (or whenever your raw text file changes) to:
  1. Preprocess the raw OCR text → cleaned_chunks.json
  2. Encode all chunks with SentenceTransformer
  3. Build and save the FAISS index

Usage (from project root):
    python scripts/build_index.py
    python scripts/build_index.py --skip-preprocess   # if chunks already exist
"""

import argparse
import logging
import sys
from pathlib import Path

# ── Make sure project root is on sys.path ─────────────────────────────────────
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.config.settings import (
    FAISS_INDEX_PATH,
    INDEX_DIR,
    METADATA_PATH,
    PROCESSED_DIR,
    RAW_DIR,
    RAW_TEXT_CANDIDATES,
    RAW_TEXT_PATH,
)
from src.ingestion.preprocessor import run_preprocessing
from src.embedding.encoder import encode_texts
from src.embedding.index_store import build_and_save_index

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Build the FAISS index from raw text.")
    p.add_argument(
        "--skip-preprocess",
        action="store_true",
        help="Skip preprocessing and reuse existing cleaned_chunks.json",
    )
    return p.parse_args()


def main() -> None:
    args = parse_args()

    print("\n" + "=" * 62)
    print("  Islamiyat RAG — Index Builder")
    print("=" * 62 + "\n")

    # ── Step 1: Preprocess ────────────────────────────────────────────────────
    if args.skip_preprocess and METADATA_PATH.exists():
        import json
        logger.info("--skip-preprocess: loading existing %s", METADATA_PATH)
        with open(METADATA_PATH, encoding="utf-8") as f:
            chunks = json.load(f)
        logger.info("Loaded %d chunks", len(chunks))
    else:
        if not RAW_TEXT_PATH.exists():
            logger.error("Raw text file not found: %s", RAW_TEXT_PATH)
            logger.error("Checked these paths:")
            for path in RAW_TEXT_CANDIDATES:
                logger.error("  - %s", path)
            sys.exit(1)

        PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
        INDEX_DIR.mkdir(parents=True, exist_ok=True)
        RAW_DIR.mkdir(parents=True, exist_ok=True)

        logger.info("Step 1/3 — Preprocessing raw text...")
        chunks = run_preprocessing(
            input_path=RAW_TEXT_PATH,
            output_path=METADATA_PATH,
            report_path=PROCESSED_DIR / "preprocessing_report.txt",
        )
        logger.info("Preprocessing complete: %d chunks", len(chunks))

    if not chunks:
        logger.error("No chunks produced — check your input file and settings.")
        sys.exit(1)

    # ── Step 2: Encode ────────────────────────────────────────────────────────
    logger.info("Step 2/3 — Encoding %d chunks with SentenceTransformer...", len(chunks))
    texts = [c["text"] for c in chunks]
    embeddings = encode_texts(texts)
    logger.info("Embeddings shape: %s", embeddings.shape)

    # ── Step 3: Build & save index ────────────────────────────────────────────
    logger.info("Step 3/3 — Building FAISS index...")
    INDEX_DIR.mkdir(parents=True, exist_ok=True)
    build_and_save_index(embeddings, str(FAISS_INDEX_PATH))
    logger.info("FAISS index saved → %s", FAISS_INDEX_PATH)

    print("\n" + "=" * 62)
    print(f"  Done!  {len(chunks)} chunks indexed.")
    print(f"  Chunks : {METADATA_PATH}")
    print(f"  Index  : {FAISS_INDEX_PATH}")
    print("=" * 62 + "\n")


if __name__ == "__main__":
    main()