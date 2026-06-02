"""Shared request/response models."""
from __future__ import annotations

from pydantic import BaseModel


class BulletRewrite(BaseModel):
    original: str
    rewritten: str


class RewriteRequest(BaseModel):
    bullets: list[str]
    job_description: str
    strictness: float = 0.5


class RewriteResponse(BaseModel):
    bullets: list[BulletRewrite]


class ExportRequest(BaseModel):
    name: str = "resume"
    bullets: list[str]


class JDExtract(BaseModel):
    skills: list[str]
    titles: list[str]
    years_experience: int | None = None
