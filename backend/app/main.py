"""Resume AI Optimizer — FastAPI entrypoint."""
from __future__ import annotations

import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import analyze, export, rewrite

app = FastAPI(title="Resume AI Optimizer", version="0.2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=os.environ.get("CORS_ORIGINS", "http://localhost:3000").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(analyze.router, prefix="/api", tags=["analyze"])
app.include_router(rewrite.router, prefix="/api", tags=["rewrite"])
app.include_router(export.router, prefix="/api", tags=["export"])


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok", "version": app.version}
