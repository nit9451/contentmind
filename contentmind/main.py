from fastapi import FastAPI

from contentmind.config import get_settings
from contentmind.memory import MemoryStore
from contentmind.schemas import ContentItem, HealthResponse, MemoryQueryResponse, MemoryRecord


def create_app(memory_store: MemoryStore | None = None) -> FastAPI:
    settings = get_settings()
    store = memory_store or MemoryStore()
    app = FastAPI(
        title=settings.app_name,
        description="Persistent memory layer for AI content pipelines.",
        version="0.1.0",
    )

    @app.get("/health", response_model=HealthResponse, tags=["system"])
    def health() -> HealthResponse:
        return HealthResponse(status="ok", service=settings.app_name)

    @app.post("/memory/ingest", response_model=MemoryRecord, tags=["memory"])
    def ingest_memory(item: ContentItem) -> MemoryRecord:
        return store.ingest(item)

    @app.get("/memory/query", response_model=MemoryQueryResponse, tags=["memory"])
    def query_memory(q: str, limit: int = 5) -> MemoryQueryResponse:
        matches = store.query(q=q, limit=limit)
        return MemoryQueryResponse(query=q, count=len(matches), results=matches)

    return app


app = create_app()
