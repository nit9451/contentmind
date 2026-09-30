# ContentMind Architecture

ContentMind is designed as a persistent memory layer for AI-assisted content workflows. The system stores reusable knowledge about a channel, audience, past content, and performance signals, then retrieves the most relevant memory before asking an LLM to generate new content.

## Design Goals

- Reduce repeated prompt setup across content sessions.
- Improve brand and style consistency across generated scripts.
- Prevent accidental repetition of topics and angles.
- Keep memory retrieval inspectable and testable.
- Separate ingestion, retrieval, context building, and generation.

## System Components

### 1. Ingestion Layer

The ingestion layer accepts raw and structured content:

- Channel profile
- Audience profile
- Past scripts
- Video titles and descriptions
- Research notes
- Analytics metadata
- Comment themes and viewer questions

The first MVP should support manual JSON ingestion before integrating external APIs.

### 2. Memory Store

The memory store should combine three kinds of information:

- Structured metadata: content type, topic, date, platform, performance signals
- Vector embeddings: semantic similarity across scripts, notes, and topics
- Graph relationships: links between topics, content pillars, audience needs, and repeated patterns

This hybrid model allows both semantic search and explicit relationship traversal.

### 3. Retrieval Engine

The retrieval engine receives a user request and returns context that is relevant, compact, and safe to inject into a prompt.

Expected retrieval steps:

1. Normalize the user request.
2. Extract topic, audience, and format signals.
3. Search semantically similar content.
4. Traverse related topics and content pillars.
5. Remove duplicates and low-value memories.
6. Rank the final context by relevance and usefulness.

### 4. Context Builder

The context builder converts retrieved memory into a generation-ready prompt block.

It should include:

- Channel positioning
- Audience summary
- Relevant previous scripts
- Style constraints
- Topic gap or duplication warnings
- Output format instructions

The output should be logged or returned for inspection so prompt quality can be improved over time.

### 5. Generation Layer

The generation layer sends the final prompt to an LLM provider such as Claude API.

Initial generation modes:

- Script outline
- Full script draft
- Topic ideas
- Hook variations
- Content repurposing plan

## MVP API Surface

```http
POST /memory/ingest
GET /memory/query
POST /generate/script
POST /generate/topics
GET /channel/profile
POST /channel/profile
```

## Data Model Sketch

```text
ChannelProfile
  id
  name
  niche
  audience
  tone
  content_pillars

ContentItem
  id
  channel_id
  type
  title
  body
  topic
  published_at
  performance_metadata

MemoryChunk
  id
  content_item_id
  chunk_text
  embedding_id
  metadata

GenerationRun
  id
  request
  retrieved_memory_ids
  prompt_context
  output
  created_at
```

## Implementation Plan

1. Create FastAPI project skeleton. Done.
2. Add Pydantic models for channel profiles and content items. Done.
3. Add memory ingestion endpoint. Done.
4. Add retrieval endpoint with simple keyword search. Done.
5. Implement local SQLite persistence. Done.
6. Upgrade retrieval to embeddings.
7. Add Claude generation endpoint.
8. Add tests for ingestion, retrieval, and context building.
9. Add Dockerfile and GitHub Actions workflow.

## Engineering Notes

- Retrieval should be deterministic enough to test.
- Prompt context should have token limits from the beginning.
- The system should expose which memories were used for each generation.
- Analytics integration should come after the local memory loop works.
- Dashboard work should wait until the backend contract is stable.
