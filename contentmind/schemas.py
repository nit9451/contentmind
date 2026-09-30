from datetime import datetime

from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: str = Field(examples=["ok"])
    service: str = Field(examples=["ContentMind"])


class ChannelProfile(BaseModel):
    name: str
    niche: str
    audience: str
    tone: str
    content_pillars: list[str] = Field(default_factory=list)


class ContentItem(BaseModel):
    title: str
    body: str
    content_type: str = "script"
    topic: str | None = None
    published_at: datetime | None = None
    performance_metadata: dict[str, float | int | str] = Field(default_factory=dict)


class GenerationRequest(BaseModel):
    topic: str
    format: str = "script"
    audience: str | None = None
    constraints: list[str] = Field(default_factory=list)
