from dataclasses import dataclass, field
from datetime import datetime
from itertools import count
import json
from pathlib import Path
import sqlite3
from urllib.parse import urlparse

from contentmind.schemas import ContentItem, MemoryRecord


@dataclass
class MemoryStore:
    """Small in-memory store for the first ContentMind MVP loop."""

    _ids: count = field(default_factory=lambda: count(1))
    _records: list[MemoryRecord] = field(default_factory=list)

    def ingest(self, item: ContentItem) -> MemoryRecord:
        record = MemoryRecord(id=next(self._ids), item=item)
        self._records.append(record)
        return record

    def query(self, q: str, limit: int = 5) -> list[MemoryRecord]:
        query_terms = self._normalize(q)
        ranked: list[tuple[int, MemoryRecord]] = []

        for record in self._records:
            haystack = self._record_text(record)
            score = sum(1 for term in query_terms if term in haystack)
            if score > 0:
                ranked.append((score, record))

        ranked.sort(key=lambda match: (-match[0], match[1].id))
        return [record for _, record in ranked[:limit]]

    def all(self) -> list[MemoryRecord]:
        return list(self._records)

    @staticmethod
    def _normalize(text: str) -> set[str]:
        return {
            token.strip(".,!?;:()[]{}\"'").lower()
            for token in text.split()
            if token.strip(".,!?;:()[]{}\"'")
        }

    @classmethod
    def _record_text(cls, record: MemoryRecord) -> set[str]:
        item = record.item
        return cls._normalize(
            " ".join(
                value
                for value in [
                    item.title,
                    item.body,
                    item.content_type,
                    item.topic or "",
                ]
                if value
            )
        )


class SQLiteMemoryStore:
    """SQLite-backed memory store for local persistent ContentMind state."""

    def __init__(self, database_url: str = "sqlite:///./contentmind.db") -> None:
        self.database_path = self._path_from_database_url(database_url)
        self.database_path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize()

    def ingest(self, item: ContentItem) -> MemoryRecord:
        with self._connect() as connection:
            cursor = connection.execute(
                """
                INSERT INTO memories (
                    title,
                    body,
                    content_type,
                    topic,
                    published_at,
                    performance_metadata
                )
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    item.title,
                    item.body,
                    item.content_type,
                    item.topic,
                    item.published_at.isoformat() if item.published_at else None,
                    json.dumps(item.performance_metadata),
                ),
            )
            connection.commit()
            record_id = cursor.lastrowid

        return MemoryRecord(id=record_id, item=item)

    def query(self, q: str, limit: int = 5) -> list[MemoryRecord]:
        query_terms = MemoryStore._normalize(q)
        ranked: list[tuple[int, MemoryRecord]] = []

        for record in self.all():
            haystack = MemoryStore._record_text(record)
            score = sum(1 for term in query_terms if term in haystack)
            if score > 0:
                ranked.append((score, record))

        ranked.sort(key=lambda match: (-match[0], match[1].id))
        return [record for _, record in ranked[:limit]]

    def all(self) -> list[MemoryRecord]:
        with self._connect() as connection:
            rows = connection.execute(
                """
                SELECT
                    id,
                    title,
                    body,
                    content_type,
                    topic,
                    published_at,
                    performance_metadata
                FROM memories
                ORDER BY id ASC
                """
            ).fetchall()

        return [self._row_to_record(row) for row in rows]

    def _initialize(self) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS memories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    body TEXT NOT NULL,
                    content_type TEXT NOT NULL,
                    topic TEXT,
                    published_at TEXT,
                    performance_metadata TEXT NOT NULL DEFAULT '{}',
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            connection.commit()

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        return connection

    @staticmethod
    def _path_from_database_url(database_url: str) -> Path:
        parsed = urlparse(database_url)
        if parsed.scheme != "sqlite":
            raise ValueError("Only sqlite database URLs are supported in the local MVP")

        if parsed.netloc and parsed.path:
            return Path(f"/{parsed.netloc}{parsed.path}").expanduser()

        path = parsed.path
        if path.startswith("/./"):
            path = path[1:]

        return Path(path or "contentmind.db").expanduser()

    @staticmethod
    def _row_to_record(row: sqlite3.Row) -> MemoryRecord:
        published_at = (
            datetime.fromisoformat(row["published_at"]) if row["published_at"] else None
        )
        item = ContentItem(
            title=row["title"],
            body=row["body"],
            content_type=row["content_type"],
            topic=row["topic"],
            published_at=published_at,
            performance_metadata=json.loads(row["performance_metadata"] or "{}"),
        )
        return MemoryRecord(id=row["id"], item=item)
