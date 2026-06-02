"""Bullet-by-bullet resume rewriting with hallucination guards."""
from __future__ import annotations

from anthropic import AsyncAnthropic
from pydantic import BaseModel

_client: AsyncAnthropic | None = None


def _get_client() -> AsyncAnthropic:
    """Build the Anthropic client lazily so imports don't require a key."""
    global _client
    if _client is None:
        _client = AsyncAnthropic()
    return _client


SYSTEM = """You rewrite resume bullets to better match a job description.

HARD RULES:
- Never invent employers, years, titles, or technologies the user didn't list.
- Keep each bullet under 28 words.
- Lead with an action verb.
- Quantify only when the original bullet had a number.
- Return JSON: {"bullets": [{"original": "...", "rewritten": "..."}, ...]}
"""


class Bullet(BaseModel):
    original: str
    rewritten: str


class RewriteResult(BaseModel):
    bullets: list[Bullet]


async def rewrite_bullets(
    bullets: list[str],
    jd: str,
    strictness: float = 0.5,
) -> RewriteResult:
    """strictness: 0 = barely touch, 1 = aggressive rewrite."""
    user = (
        f"JOB DESCRIPTION:\n{jd}\n\n"
        f"STRICTNESS: {strictness}\n\n"
        f"BULLETS TO REWRITE:\n" + "\n".join(f"- {b}" for b in bullets)
    )
    res = await _get_client().messages.create(
        model="claude-sonnet-4-6",
        max_tokens=2000,
        system=SYSTEM,
        messages=[{"role": "user", "content": user}],
    )
    text = res.content[0].text
    return RewriteResult.model_validate_json(text)
