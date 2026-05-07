import json
import re
from pathlib import Path
from typing import Any

from src.config.settings import CHUNK_OVERLAP, CHUNK_SIZE
from src.ingestion.chunker import chunk_text, normalize_whitespace

CHAPTER_PATTERN = re.compile(r"^##\s*CHAPTER\s*\d+\s*:\s*(.+)$", re.IGNORECASE)
LESSON_PATTERN = re.compile(r"^###\s*سبق\s*\d+\s*:\s*(.+)$", re.IGNORECASE)
CONTENT_MARKER_PATTERN = re.compile(r"^###\s*📘\s*Lesson\s*Content\s*:\s*$", re.IGNORECASE)


def parse_sections(raw_text: str) -> list[dict[str, Any]]:
    sections: list[dict[str, Any]] = []
    current: dict[str, Any] = {"chapter": "", "lesson": "", "lines": []}

    for raw_line in raw_text.splitlines():
        line = raw_line.strip()
        if not line:
            if current["lines"] and current["lines"][-1] != "":
                current["lines"].append("")
            continue

        if CONTENT_MARKER_PATTERN.match(line):
            continue

        chapter_match = CHAPTER_PATTERN.match(line)
        lesson_match = LESSON_PATTERN.match(line)
        if chapter_match:
            if current["lines"]:
                sections.append(current.copy())
            current = {"chapter": chapter_match.group(1).strip(), "lesson": "", "lines": []}
            continue

        if lesson_match:
            if current["lines"]:
                sections.append(current.copy())
            current["lesson"] = lesson_match.group(1).strip()
            current["lines"] = []
            continue

        current["lines"].append(line)

    if current["lines"]:
        sections.append(current)
    return sections


def build_chunk_metadata(sections: list[dict[str, Any]]) -> list[dict[str, Any]]:
    chunks: list[dict[str, Any]] = []
    chunk_id = 0

    for section in sections:
        section_text = normalize_whitespace("\n".join(section["lines"]))
        if not section_text:
            continue

        for part in chunk_text(section_text, CHUNK_SIZE, CHUNK_OVERLAP):
            chunk_id += 1
            chunks.append(
                {
                    "text": part,
                    "chapter": section.get("chapter", ""),
                    "lesson": section.get("lesson", ""),
                    "section_type": "lesson",
                    "chunk_id": str(chunk_id),
                }
            )
    return chunks


def run_preprocessing(input_path: Path, output_path: Path, report_path: Path) -> list[dict[str, Any]]:
    raw_text = input_path.read_text(encoding="utf-8")
    sections = parse_sections(raw_text)
    chunks = build_chunk_metadata(sections)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(chunks, ensure_ascii=False, indent=2), encoding="utf-8")

    report_path.parent.mkdir(parents=True, exist_ok=True)
    with report_path.open("w", encoding="utf-8") as report_file:
        report_file.write(f"source: {input_path}\n")
        report_file.write(f"raw characters: {len(raw_text)}\n")
        report_file.write(f"sections: {len(sections)}\n")
        report_file.write(f"chunks: {len(chunks)}\n")

    return chunks
