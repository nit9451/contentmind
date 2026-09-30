from fastapi.testclient import TestClient

from contentmind.main import create_app
from contentmind.memory import MemoryStore


def test_memory_ingest_stores_content_item() -> None:
    client = TestClient(create_app(memory_store=MemoryStore()))

    response = client.post(
        "/memory/ingest",
        json={
            "title": "AI thumbnail tools",
            "body": "A script about image generation tools for YouTube thumbnails.",
            "content_type": "script",
            "topic": "AI image tools",
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["id"] == 1
    assert payload["item"]["title"] == "AI thumbnail tools"
    assert payload["item"]["topic"] == "AI image tools"


def test_memory_query_returns_relevant_records() -> None:
    client = TestClient(create_app(memory_store=MemoryStore()))
    client.post(
        "/memory/ingest",
        json={
            "title": "AI thumbnail tools",
            "body": "A script about image generation tools for YouTube thumbnails.",
            "topic": "AI image tools",
        },
    )
    client.post(
        "/memory/ingest",
        json={
            "title": "Backend deployment checklist",
            "body": "A checklist for deploying FastAPI services.",
            "topic": "deployment",
        },
    )

    response = client.get("/memory/query", params={"q": "AI thumbnails", "limit": 3})

    assert response.status_code == 200
    payload = response.json()
    assert payload["query"] == "AI thumbnails"
    assert payload["count"] == 1
    assert payload["results"][0]["item"]["title"] == "AI thumbnail tools"
