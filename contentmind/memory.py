from dataclasses import dataclass, field
from itertools import count

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
