# AutoMind AI 🚗

An educational automotive knowledge assistant prototype. The first milestone implements document ingestion, source-aware chunking, TF-IDF retrieval, and a FastAPI endpoint that returns relevant evidence passages.

> **Project status:** Early-stage prototype. It is not an OEM tool or official automotive diagnostic system. Do not use it to make safety-critical repair or driving decisions.

## What works today

- Load Markdown and plain-text documents from a local corpus.
- Split documents into overlapping chunks while preserving source filenames and chunk IDs.
- Rank passages with a transparent TF-IDF/cosine-similarity baseline.
- Query the index through a small FastAPI service.
- Return source metadata and scores so results can be inspected.
- Run automated tests locally or through GitHub Actions.

This is **retrieval-only** today. It does not generate answers with an LLM yet. We will benchmark the baseline before introducing embeddings and generation.

## Quick start

Requires Python 3.10 or newer.

```bash
python -m venv .venv
```

Activate the environment:

```powershell
# Windows PowerShell
.venv\Scripts\Activate.ps1
```

```bash
# macOS/Linux
source .venv/bin/activate
```

Install the package and development tools, then run the tests:

```bash
python -m pip install -e ".[dev]"
python -m pytest
```

Start the API:

```bash
uvicorn automind_ai.api:app --reload
```

Open the interactive API docs at http://127.0.0.1:8000/docs.

## Try a query

```bash
curl -X POST "http://127.0.0.1:8000/query" \
  -H "Content-Type: application/json" \
  -d '{"question":"What does ABS do?","top_k":3}'
```

The response includes retrieved passages, relative source paths, chunk IDs, and relevance scores. The included sample file is synthetic demo content, not a vehicle manual.

## Current architecture

```text
Local Markdown/TXT files
        |
        v
Document loader and chunker
        |
        v
TF-IDF index
        |
        v
FastAPI /query
        |
        v
Ranked source passages + metadata
```

## Roadmap

- [x] Define source-aware chunk data model.
- [x] Load Markdown and plain-text sources.
- [x] Implement overlapping chunking.
- [x] Build TF-IDF retrieval baseline.
- [x] Add FastAPI health and query endpoints.
- [x] Add tests and continuous integration.
- [ ] Add a labelled retrieval evaluation set.
- [ ] Measure Recall@k and reciprocal rank on the evaluation set.
- [ ] Add configurable corpus paths and richer section/page metadata.
- [ ] Compare lexical retrieval with embedding-based retrieval.
- [ ] Add citations-aware LLM answer generation with an explicit insufficient-evidence response.
- [ ] Evaluate answer groundedness, latency, and failure cases.

## Safety and data policy

- Use public, licensed, or otherwise authorised documents only.
- Do not upload private or proprietary vehicle documents without permission.
- Treat retrieved passages as informational references, not authoritative repair instructions.
- The system should acknowledge when the indexed corpus does not support an answer.
- Generated text or enhanced imagery must not be treated as evidence of vehicle damage or safety condition.

## Project log

See [LEARNING_LOG.md](LEARNING_LOG.md) for implementation notes, decisions, and next steps.

## License

A license will be selected once source-data and dependency choices are finalised.
