from pathlib import Path

import pytest

from automind_ai.documents import chunk_text, load_text_documents


def test_chunk_text_preserves_source_and_chunk_ids():
    chunks = chunk_text(
        "one two three four five six seven",
        source="manual.md",
        chunk_size_words=4,
        overlap_words=1,
    )
    assert [chunk.chunk_id for chunk in chunks] == [0, 1]
    assert [chunk.source for chunk in chunks] == ["manual.md", "manual.md"]
    assert chunks[0].text == "one two three four"
    assert chunks[1].text == "four five six seven"


def test_chunk_text_rejects_invalid_overlap():
    with pytest.raises(ValueError):
        chunk_text("some words", source="x.md", chunk_size_words=4, overlap_words=4)


def test_loader_reads_supported_files_and_skips_others(tmp_path: Path):
    (tmp_path / "system.md").write_text("ABS wheel speed sensor", encoding="utf-8")
    (tmp_path / "notes.txt").write_text("Battery management system", encoding="utf-8")
    (tmp_path / "ignored.pdf").write_bytes(b"not parsed by the first version")
    (tmp_path / ".hidden.md").write_text("hidden words", encoding="utf-8")
    chunks = load_text_documents(tmp_path, chunk_size_words=20, overlap_words=2)
    assert {chunk.source for chunk in chunks} == {"system.md", "notes.txt"}
    assert len(chunks) == 2


def test_missing_directory_returns_empty_list(tmp_path: Path):
    assert load_text_documents(tmp_path / "missing") == []
