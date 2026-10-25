"""A simple lexical retrieval baseline for AutoMind AI."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from automind_ai.documents import DocumentChunk


@dataclass(frozen=True, slots=True)
class SearchResult:
    source: str
    chunk_id: int
    score: float
    text: str


class TfidfRetriever:
    """Rank passages by TF-IDF cosine similarity before adding semantic search."""
    def __init__(self, chunks: Sequence[DocumentChunk]) -> None:
        self._chunks = list(chunks)
        self._vectorizer: TfidfVectorizer | None = None
        self._matrix = None
        if not self._chunks:
            return

        vectorizer = TfidfVectorizer(stop_words="english")
        try:
            matrix = vectorizer.fit_transform([chunk.text for chunk in self._chunks])
        except ValueError:
            # Punctuation-only documents or all-stopword text can yield no vocabulary.
            return
        self._vectorizer = vectorizer
        self._matrix = matrix

    def search(self, query: str, *, top_k: int = 3) -> list[SearchResult]:
        """Return matching passages in descending relevance order."""
        if top_k < 1:
            raise ValueError("top_k must be at least 1")
        if not query.strip() or self._vectorizer is None or self._matrix is None:
            return []

        query_vector = self._vectorizer.transform([query])
        scores = cosine_similarity(query_vector, self._matrix).ravel()
        ranked = sorted(range(len(scores)), key=lambda i: (-float(scores[i]), i))
        results: list[SearchResult] = []
        for index in ranked:
            score = float(scores[index])
            if score <= 0:
                continue
            chunk = self._chunks[index]
            results.append(SearchResult(chunk.source, chunk.chunk_id, score, chunk.text))
            if len(results) >= top_k:
                break
        return results
