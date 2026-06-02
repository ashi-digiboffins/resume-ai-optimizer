"""Standalone rewrite + JD-extraction endpoints."""
from __future__ import annotations

from fastapi import APIRouter

from app.schemas import JDExtract, RewriteRequest, RewriteResponse
from app.services import jd_extractor, rewriter

router = APIRouter()


@router.post("/rewrite", response_model=RewriteResponse)
async def rewrite(req: RewriteRequest) -> RewriteResponse:
    result = await rewriter.rewrite_bullets(
        req.bullets, req.job_description, req.strictness
    )
    return RewriteResponse(bullets=result.model_dump()["bullets"])


@router.post("/extract", response_model=JDExtract)
async def extract(job_description: str) -> JDExtract:
    return jd_extractor.extract(job_description)
