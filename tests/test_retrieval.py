import pytest

from automind_ai.documents import DocumentChunk
from automind_ai.retrieval import TfidfRetriever


def test_search_ranks_relevant_passage_and_keeps_source():
    chunks = [
        DocumentChunk("brakes.md", 0, "ABS prevents wheel lock during braking."),
        DocumentChunk("battery.md", 0, "A battery management system monitors cell voltage and temperature."),
    ]
    results = TfidfRetriever(chunks).search("ABS wheel braking", top_k=2)
    assert results
    assert results[0].source == "brakes.md"
    assert results[0].score > 0
    assert len(results) == 1


def test_search_returns_empty_for_blank_or_unmatched_queries():
    retriever = TfidfRetriever([DocumentChunk("sample.md", 0, "vehicle battery temperature")])
    assert retriever.search("   ") == []
    assert retriever.search("pineapple spaceship") == []


def test_top_k_must_be_positive():
    with pytest.raises(ValueError):
        TfidfRetriever([]).search("anything", top_k=0)
