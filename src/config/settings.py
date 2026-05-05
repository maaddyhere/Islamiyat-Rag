import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR       = Path(__file__).resolve().parent.parent.parent
DATA_DIR       = BASE_DIR / "data"
RAW_DIR        = DATA_DIR / "raw"
PROCESSED_DIR  = DATA_DIR / "processed"
INDEX_DIR      = DATA_DIR / "index"
RAW_TEXT_PATH    = RAW_DIR / "Islamiyat_ocr_txt.txt"
METADATA_PATH    = PROCESSED_DIR / "cleaned_chunks.json"
FAISS_INDEX_PATH = INDEX_DIR / "vector_store.index"
CHUNK_SIZE    = 800
CHUNK_OVERLAP = 150
TOP_K             = 8
MAX_L2_DISTANCE   = 1.42
MAX_CONTEXT_CHARS = 6000
EMBEDDING_MODEL = "paraphrase-multilingual-mpnet-base-v2"
LLM_MODEL       = "llama-3.3-70b-versatile"
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
HF_TOKEN     = os.getenv("HF_TOKEN", "")