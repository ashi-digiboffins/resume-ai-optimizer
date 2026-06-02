"""Heuristic job-description extractor — skills, titles, years of experience.

Deliberately dependency-free: a curated skill vocabulary plus a couple of
regexes covers the vast majority of tech JDs without an LLM call.
"""
from __future__ import annotations

import re

from app.schemas import JDExtract

_SKILLS = [
    "python", "typescript", "javascript", "react", "next.js", "node", "go",
    "rust", "java", "kotlin", "swift", "fastapi", "django", "flask", "postgres",
    "postgresql", "mysql", "redis", "clickhouse", "kafka", "rabbitmq", "docker",
    "kubernetes", "terraform", "aws", "gcp", "azure", "graphql", "rest", "grpc",
    "tailwind", "playwright", "pytest", "ci/cd", "langchain", "langgraph",
    "pgvector", "llm", "rag", "stripe", "supabase",
]

_TITLES = [
    "software engineer", "senior software engineer", "staff engineer",
    "backend engineer", "frontend engineer", "full stack engineer",
    "full-stack engineer", "data engineer", "ml engineer", "devops engineer",
    "platform engineer", "engineering manager",
]

_YEARS = re.compile(r"(\d+)\+?\s*(?:years|yrs)", re.IGNORECASE)


def extract(jd: str) -> JDExtract:
    low = jd.lower()
    skills = [s for s in _SKILLS if re.search(rf"(?<!\w){re.escape(s)}(?!\w)", low)]
    titles = [t for t in _TITLES if t in low]

    years_matches = [int(m) for m in _YEARS.findall(jd)]
    years = max(years_matches) if years_matches else None

    return JDExtract(skills=skills, titles=titles, years_experience=years)
