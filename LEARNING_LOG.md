# AutoMind AI Learning Log

## 2026-10-25: Repository bootstrap and retrieval baseline

### Built
- Added a Python package using a src layout.
- Added Markdown/plain-text ingestion with stable relative source names.
- Added overlapping word-based chunking and chunk IDs.
- Added TF-IDF/cosine similarity retrieval as an explainable baseline.
- Added FastAPI health and query endpoints.
- Added synthetic demo content and tests for ingestion, retrieval, and API behavior.

### Design decisions
- Start with retrieval-only rather than generated answers, so we have a baseline to measure.
- Preserve source file and chunk ID in each result.
- Keep synthetic demo content separate from real vehicle documentation.
- Clearly label the prototype as educational and not suitable for safety-critical decisions.
- Support Markdown and TXT first. PDF parsing and page-level citations are follow-up tasks.

### Next tasks
1. Run the test suite locally and fix any issues.
2. Add a small labelled retrieval evaluation set.
3. Record baseline metrics such as Recall@k and reciprocal rank.
4. Add configurable document paths and richer source metadata.
5. Compare the TF-IDF baseline with embedding-based retrieval.
6. Add an LLM generation layer only after citations and evaluation are in place.

### Commands
```bash
python -m venv .venv
# Windows PowerShell: .venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate
python -m pip install -e ".[dev]"
pytest
uvicorn automind_ai.api:app --reload
```
