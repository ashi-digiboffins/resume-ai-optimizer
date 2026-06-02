"""ATS keyword coverage scoring.

Treats the JD as the source of truth and measures how much of its
weighted vocabulary the resume contains.
"""
from __future__ import annotations

import re
from collections import Counter
from dataclasses import dataclass

# Cheap, dependency-free stopword list — good enough for ATS keyword work.
STOPWORDS = set(
    "a an the and or but of for to with on in at by from as is are was were "
    "be been being do does did have has had this that these those it its".split()
)


@dataclass
class ATSResult:
    score: float  # 0..100
    matched: list[str]
    missing: list[str]
    weights: dict[str, int]


def _tokens(text: str) -> list[str]:
    return [t for t in re.findall(r"[A-Za-z][A-Za-z+#\-.]{1,}", text.lower()) if t not in STOPWORDS]


def score(jd: str, resume: str, top_n_keywords: int = 40) -> ATSResult:
    jd_counts = Counter(_tokens(jd))
    # Hot keywords: appear 2+ times in JD and aren't single letters.
    keywords = [k for k, v in jd_counts.most_common() if v >= 2 and len(k) > 2]
    keywords = keywords[:top_n_keywords]

    resume_set = set(_tokens(resume))
    matched = [k for k in keywords if k in resume_set]
    missing = [k for k in keywords if k not in resume_set]

    total_weight = sum(jd_counts[k] for k in keywords) or 1
    matched_weight = sum(jd_counts[k] for k in matched)
    pct = round((matched_weight / total_weight) * 100, 1)

    return ATSResult(
        score=pct,
        matched=matched,
        missing=missing,
        weights={k: jd_counts[k] for k in keywords},
    )
