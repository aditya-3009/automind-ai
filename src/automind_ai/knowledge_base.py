"""Compose ingestion and retrieval into a small knowledge base."""
from __future__ import annotations

from pathlib import Path

from automind_ai.documents import DocumentChunk, load_text_documents
from automind_ai.retrieval import SearchResult, TfidfRetriever


class KnowledgeBase:
    """An in-memory knowledge base built from local Markdown/TXT documents."""
    def __init__(self, chunks: list[DocumentChunk]) -> None:
        self._chunks = chunks
        self._retriever = TfidfRetriever(chunks)

    @classmethod
    def from_directory(cls, directory: str | Path) -> "KnowledgeBase":
        return cls(load_text_documents(directory))

    @property
    def document_count(self) -> int:
        """Return the number of indexed chunks, not original files."""
        return len(self._chunks)

    def search(self, question: str, *, top_k: int = 3) -> list[SearchResult]:
        return self._retriever.search(question, top_k=top_k)
