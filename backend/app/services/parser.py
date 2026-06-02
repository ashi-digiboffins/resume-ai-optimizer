"""Resume parsing — bytes (PDF/DOCX/TXT) → plaintext + extracted bullets."""
from __future__ import annotations

import io
import re
from dataclasses import dataclass

_BULLET_PREFIX = re.compile(r"^\s*[-*•▪●·]\s+(.*)$")
# A PII scrubber for "anonymous mode" — emails, phones, and URLs.
_EMAIL = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")
_PHONE = re.compile(r"\+?\d[\d\s().-]{7,}\d")
_URL = re.compile(r"https?://\S+")


@dataclass
class ParsedResume:
    plaintext: str
    bullets: list[str]


def parse(data: bytes, filename: str) -> ParsedResume:
    text = _extract_text(data, filename)
    return ParsedResume(plaintext=text, bullets=_extract_bullets(text))


def strip_pii(text: str) -> str:
    text = _EMAIL.sub("[email]", text)
    text = _URL.sub("[url]", text)
    text = _PHONE.sub("[phone]", text)
    return text


def _extract_text(data: bytes, filename: str) -> str:
    name = filename.lower()
    if name.endswith(".pdf"):
        return _from_pdf(data)
    if name.endswith(".docx"):
        return _from_docx(data)
    return data.decode("utf-8", errors="replace")


def _from_pdf(data: bytes) -> str:
    import pdfplumber

    out: list[str] = []
    with pdfplumber.open(io.BytesIO(data)) as pdf:
        for page in pdf.pages:
            out.append(page.extract_text() or "")
    return "\n".join(out)


def _from_docx(data: bytes) -> str:
    from docx import Document

    doc = Document(io.BytesIO(data))
    return "\n".join(p.text for p in doc.paragraphs)


def _extract_bullets(text: str) -> list[str]:
    bullets: list[str] = []
    for line in text.splitlines():
        m = _BULLET_PREFIX.match(line)
        if m:
            bullets.append(m.group(1).strip())
            continue
        # Lines that read like accomplishments even without a marker: start with
        # a capitalised verb and are reasonably long.
        stripped = line.strip()
        if 40 <= len(stripped) <= 240 and re.match(r"^[A-Z][a-z]+ed\b|^[A-Z][a-z]+", stripped):
            if any(stripped.startswith(v) for v in _ACTION_VERBS):
                bullets.append(stripped)
    return bullets


_ACTION_VERBS = (
    "Led", "Built", "Designed", "Developed", "Shipped", "Improved", "Reduced",
    "Increased", "Managed", "Created", "Implemented", "Launched", "Owned",
    "Drove", "Architected", "Optimized", "Migrated", "Automated",
)
