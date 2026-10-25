"""Load local text documents and split them into traceable chunks."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

SUPPORTED_SUFFIXES = {".md", ".txt"}


@dataclass(frozen=True, slots=True)
class DocumentChunk:
    """A text passage with metadata to trace it to its source file."""
    source: str
    chunk_id: int
    text: str


def chunk_text(
    text: str,
    *,
    source: str,
    chunk_size_words: int = 180,
    overlap_words: int = 30,
) -> list[DocumentChunk]:
    """Split text into overlapping word windows."""
    if chunk_size_words < 1:
        raise ValueError("chunk_size_words must be at least 1")
    if overlap_words < 0 or overlap_words >= chunk_size_words:
        raise ValueError("overlap_words must be >= 0 and smaller than chunk_size_words")

    words = text.split()
    if not words:
        return []

    chunks: list[DocumentChunk] = []
    step = chunk_size_words - overlap_words
    for start in range(0, len(words), step):
        window = words[start : start + chunk_size_words]
        if not window:
            break
        chunks.append(DocumentChunk(source=source, chunk_id=len(chunks), text=" ".join(window)))
        if start + chunk_size_words >= len(words):
            break
    return chunks


def load_text_documents(
    directory: str | Path,
    *,
    chunk_size_words: int = 180,
    overlap_words: int = 30,
) -> list[DocumentChunk]:
    """Load Markdown/TXT files recursively, retaining relative source paths."""
    root = Path(directory)
    if not root.exists():
        return []
    if not root.is_dir():
        raise NotADirectoryError(f"Document source is not a directory: {root}")

    chunks: list[DocumentChunk] = []
    for path in sorted(root.rglob("*")):
        if not path.is_file() or path.name.startswith("."):
            continue
        if path.suffix.lower() not in SUPPORTED_SUFFIXES:
            continue
        text = path.read_text(encoding="utf-8", errors="replace").strip()
        relative_source = path.relative_to(root).as_posix()
        chunks.extend(chunk_text(
            text, source=relative_source,
            chunk_size_words=chunk_size_words, overlap_words=overlap_words,
        ))
    return chunks
