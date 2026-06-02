"""Analyze endpoint — score + rewrite suggestions."""
from fastapi import APIRouter, File, Form, UploadFile

from app.services import ats_score, parser, rewriter

router = APIRouter()


@router.post("/analyze")
async def analyze(
    resume: UploadFile = File(...),
    job_description: str = Form(...),
    strictness: float = Form(0.5),
):
    raw = await resume.read()
    parsed = parser.parse(raw, filename=resume.filename or "resume")
    s = ats_score.score(job_description, parsed.plaintext)
    bullets = parsed.bullets[:30]  # don't blow the LLM budget
    rewrites = await rewriter.rewrite_bullets(bullets, job_description, strictness)
    return {
        "score": s.score,
        "matched_keywords": s.matched,
        "missing_keywords": s.missing,
        "rewrites": rewrites.model_dump()["bullets"],
    }
