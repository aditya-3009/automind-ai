# AutoMind AI 🚗

An educational automotive knowledge assistant that uses retrieval-augmented generation (RAG) to answer questions from a curated collection of vehicle documents and explain which sources support each answer.

> **Project status:** Early-stage prototype. This is a learning and research project, not an official automotive diagnostic system. It must not be used to make safety-critical repair or driving decisions.

## Goals

- Ingest permitted automotive documents and preserve source metadata.
- Split documents into searchable chunks and build a retrieval index.
- Retrieve relevant passages for a user's question.
- Generate answers grounded in retrieved evidence, with document and page/section references where available.
- Measure retrieval quality, answer grounding, latency, and common failure cases.
- Expose the workflow through a small API once the retrieval pipeline is working.

## Planned architecture

1. **Document ingestion**: load public or otherwise permitted manuals and technical documents.
2. **Chunking and metadata**: split text into useful passages while retaining source, section, page, and document identifiers.
3. **Retrieval**: embed passages and rank relevant chunks for each query.
4. **Answer generation**: provide the retrieved evidence to an LLM and require it to distinguish evidence from uncertainty.
5. **Citations and guardrails**: show source references, report when evidence is insufficient, and avoid presenting generated content as authoritative repair advice.
6. **Evaluation**: run a small labelled question set and track retrieval and response quality.
7. **API / interface**: add a testable interface after the core pipeline is validated.

## Initial milestones

- [ ] Define the document and chunk data models.
- [ ] Add a small, legally usable sample corpus.
- [ ] Implement ingestion and text extraction.
- [ ] Implement chunking with source metadata.
- [ ] Build a baseline retrieval pipeline.
- [ ] Return answers with source references.
- [ ] Add tests for ingestion, retrieval, citations, and empty results.
- [ ] Create an evaluation dataset and record baseline metrics.
- [ ] Add a FastAPI endpoint and usage examples.

## Proposed stack

Python, a document parsing library, an embedding model, a vector index, an LLM provider abstraction, FastAPI, pytest, and GitHub Actions. The exact components will be selected and documented as the prototype develops.

## Safety and data policy

- Use public, licensed, or otherwise authorised source documents.
- Do not upload private, proprietary, or copyrighted documents without permission.
- Treat retrieval results as informational material, not definitive instructions.
- If the sources do not support an answer, the system should say so.
- Image enhancement or generated text must not be treated as evidence of vehicle damage or safety condition.

## Development

Project setup and implementation instructions will be added as the first working components are completed. See [LEARNING_LOG.md](LEARNING_LOG.md) for progress and decisions.

## License

License to be selected once source-data and dependency choices are finalised.
