"""
Interactive query loop:
    python scripts/query.py
"""
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