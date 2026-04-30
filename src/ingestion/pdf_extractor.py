import os, subprocess, shutil
from langchain_core.documents import Document
from src.config.settings import PDF_PATH

BIDI_CONTROLS = (
    '\u200e', '\u200f', '\u202a', '\u202b', '\u202c',
    '\u202d', '\u202e', '\u2066', '\u2067', '\u2068', '\u2069',
)

def extract_text(pdf_path=PDF_PATH) -> str:
    pdftotext = shutil.which("pdftotext")
    if not pdftotext:
        raise FileNotFoundError("poppler-utils not installed")
    proc = subprocess.run(
        [pdftotext, "-enc", "UTF-8", str(pdf_path), "-"],
        capture_output=True, text=True, encoding="utf-8", errors="replace"
    )
    if proc.returncode != 0:
        raise RuntimeError(f"pdftotext failed: {proc.stderr}")
    return "".join(ch for ch in proc.stdout if ch not in BIDI_CONTROLS)

def build_documents(full_text: str, pdf_path=PDF_PATH) -> list[Document]:
    pages = full_text.split("\x0c")
    docs = []
    for i, text in enumerate(pages):
        text = text.strip()
        if text:
            docs.append(Document(
                page_content=text,
                metadata={"source": os.path.basename(pdf_path), "page": i + 1}
            ))
    return docs