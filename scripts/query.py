"""
Interactive query loop:
    python scripts/query.py
"""
import sys
from pathlib import Path

# ── Make sure project root is on sys.path ─────────────────────────────────────
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.pipeline.rag_pipeline import RAGPipeline

def main():
    pipeline = RAGPipeline()   # loads index + model once
    print("RAG ready. Type 'exit' to quit.\n")
    while True:
        query = input("سوال: ").strip()
        if query.lower() in ("exit", "quit", "q"):
            break
        if query:
            pipeline.run(query)

if __name__ == "__main__":
    main()