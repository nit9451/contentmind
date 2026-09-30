# ContentMind

Persistent memory layer for AI content pipelines.

ContentMind is a product and architecture concept for giving AI content workflows long-term memory. Instead of repeating brand context, audience details, past content history, and style rules in every prompt, ContentMind stores that knowledge once and retrieves the right context before generation.

[![Project Status](https://img.shields.io/badge/status-architecture%20spec-blue)](https://github.com/nit9451/contentmind)
[![AI Focus](https://img.shields.io/badge/focus-RAG%20%2B%20memory-4f46e5)](https://github.com/nit9451/contentmind)
[![Backend](https://img.shields.io/badge/backend-FastAPI-009688)](https://fastapi.tiangolo.com/)
[![LLM](https://img.shields.io/badge/LLM-Claude%20API-d97757)](https://www.anthropic.com/)

## Problem

Most AI content workflows are stateless. Every new session starts with repeated setup:

- What the channel is about
- Who the audience is
- What tone and format to use
- Which topics have already been covered
- Which hooks, formats, and angles performed well

That repeated context makes prompting slower, less reliable, and harder to scale.

## Solution

ContentMind acts as a memory layer between a content workflow and an LLM. It stores structured channel knowledge, historical scripts, topic relationships, and audience signals, then retrieves relevant context before each generation request.

```text
Content inputs
  -> ingestion layer
  -> graph/vector memory
  -> retrieval and ranking
  -> prompt context builder
  -> Claude/API generation
  -> script, outline, or content plan
```

The goal is simple: keep creative output consistent without forcing the user to re-explain the same context every time.

## Core Use Cases

| Use case | What ContentMind remembers | Output |
| --- | --- | --- |
| Script generation | Channel voice, audience, past scripts, topic gaps | On-brand video scripts |
| Topic planning | Covered topics, clusters, performance signals | New content ideas |
| Style consistency | Hook style, pacing, recurring phrases, format rules | Brand-aligned drafts |
| Avoid repetition | Similar historical topics and angles | Duplicate-topic warnings |
| Content research | Notes, sources, previous conclusions | Reusable context blocks |

## Architecture

```text
                           ContentMind

  Ingestion Layer
  - channel profile
  - scripts and outlines
  - content pillars
  - audience notes
  - analytics metadata
          |
          v
  Memory Store
  - graph relationships for entities and topics
  - vector search for semantic retrieval
  - structured metadata for filtering
          |
          v
  Retrieval Engine
  - query understanding
  - hybrid graph/vector lookup
  - deduplication
  - relevance ranking
          |
          v
  Context Builder
  - selected memories
  - brand/style constraints
  - previous-topic warnings
  - generation instructions
          |
          v
  Generation Layer
  - Claude API
  - script generation
  - outline generation
  - topic planning
```

More detail: [docs/architecture.md](docs/architecture.md)

## Planned Tech Stack

| Layer | Technology | Purpose |
| --- | --- | --- |
| API | FastAPI | REST endpoints for ingestion, retrieval, and generation |
| Language | Python 3.11+ | Core backend and pipeline logic |
| LLM | Claude API | Content generation with retrieved memory context |
| Memory | Cognee or graph/vector store | Hybrid relationship and semantic memory |
| Data | SQLite first, PostgreSQL later | Local development and production-ready metadata storage |
| Testing | Pytest | Retrieval and prompt-building validation |
| DevOps | Docker, GitHub Actions | Repeatable setup and CI checks |

## Target API Shape

```http
POST /memory/ingest
```

Stores channel profiles, scripts, outlines, research notes, and performance metadata.

```http
GET /memory/query?q=ai-video-tools&limit=5
```

Returns relevant memories for a topic or generation request.

```http
POST /generate/script
```

Builds memory-aware prompt context and generates a script draft.

## Example Memory Flow

```python
channel_profile = {
    "name": "@pranitz.ai",
    "niche": "AI tools for creators",
    "audience": "solopreneurs, developers, and content creators",
    "tone": "practical, concise, educational"
}

generation_request = {
    "topic": "Best AI image tools for YouTube thumbnails",
    "format": "8 minute YouTube script"
}

# ContentMind retrieves relevant channel memory, previous topics,
# preferred hook formats, and duplicate-topic warnings before generation.
```

## Repository Status

This repository contains the architecture direction and an initial FastAPI implementation. The current implementation exposes a health endpoint, memory ingestion, simple in-memory retrieval, and schema models that will support the larger agent workflow.

## Build Roadmap

| Phase | Goal | Status |
| --- | --- | --- |
| 1 | Define architecture, use cases, and API shape | Done |
| 2 | Create FastAPI skeleton and configuration | Done |
| 3 | Implement local memory ingestion | Done |
| 4 | Add simple memory retrieval | Done |
| 5 | Add semantic retrieval and ranking | Planned |
| 6 | Add Claude generation pipeline | Planned |
| 7 | Add tests, Docker, and CI | Planned |
| 8 | Add dashboard or CLI workflow | Planned |

## Tech Lead Notes

Key design decisions:

- Start with a small backend-first MVP before adding a dashboard.
- Keep memory ingestion separate from generation so each part can be tested independently.
- Store structured metadata alongside embeddings so retrieval can filter by content type, audience, channel, and topic cluster.
- Add duplicate-topic detection early because it creates immediate value for content planning.
- Treat prompt context as a generated artifact that can be inspected, tested, and improved.

## Local Development

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest
uvicorn contentmind.main:app --reload
```

## Current API

```http
GET /health
POST /memory/ingest
GET /memory/query?q=ai-thumbnails&limit=5
```

The current memory store is intentionally in-memory for the first MVP. The next backend step is persistence with SQLite or PostgreSQL.

## Why This Project Matters

ContentMind demonstrates practical AI engineering beyond a simple chatbot:

- Persistent memory design
- RAG-style retrieval
- Context engineering
- API design
- Product thinking
- Roadmap planning
- Maintainable backend architecture

## Author

Nitish Purohit  
Senior Full Stack Engineer with 6+ years of experience and 2.5 years of focused AI engineering experience.

- GitHub: [github.com/nit9451](https://github.com/nit9451)
- Portfolio: [nit9451.github.io](https://nit9451.github.io/)
