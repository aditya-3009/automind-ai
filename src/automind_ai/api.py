"""FastAPI interface for the retrieval-only AutoMind AI prototype."""
from pathlib import Path

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from automind_ai.knowledge_base import KnowledgeBase

PROJECT_ROOT = Path(__file__).resolve().parents[2]
SAMPLE_DOCUMENTS = PROJECT_ROOT / "data" / "sample_docs"

app = FastAPI(
    title="AutoMind AI",
    description=(
        "Educational automotive document retrieval prototype. "
        "Returns source passages and is not an official diagnostic tool."
    ),
    version="0.1.0",
)
knowledge_base = KnowledgeBase.from_directory(SAMPLE_DOCUMENTS)


class QueryRequest(BaseModel):
    question: str = Field(min_length=1, max_length=1000)
    top_k: int = Field(default=3, ge=1, le=10)


class SourcePassage(BaseModel):
    source: str
    chunk_id: int
    score: float
    text: str


class QueryResponse(BaseModel):
    question: str
    result_count: int
    results: list[SourcePassage]
    mode: str = "retrieval_only"
    note: str = "Retrieved passages are evidence references, not a generated diagnosis or repair instruction."


@app.get("/health")
def health() -> dict[str, str | int]:
    return {"status": "ok", "indexed_chunks": knowledge_base.document_count}


@app.post("/query", response_model=QueryResponse)
def query_documents(request: QueryRequest) -> QueryResponse:
    if not request.question.strip():
        raise HTTPException(status_code=422, detail="Question must contain non-whitespace text")
    matches = knowledge_base.search(request.question, top_k=request.top_k)
    passages = [
        SourcePassage(
            source=item.source, chunk_id=item.chunk_id,
            score=round(item.score, 6), text=item.text,
        )
        for item in matches
    ]
    return QueryResponse(
        question=request.question, result_count=len(passages), results=passages,
    )
