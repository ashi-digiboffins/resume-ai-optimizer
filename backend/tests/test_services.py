from app.services import jd_extractor
from app.services.ats_score import score
from app.services.parser import ParsedResume, parse, strip_pii


def test_ats_score_matches_keywords():
    jd = "Python FastAPI Postgres Docker are core here Python FastAPI Postgres Docker matter"
    resume = "Built Python services with FastAPI and Postgres"
    result = score(jd, resume)
    assert "python" in result.matched
    assert "docker" in result.missing
    assert 0 <= result.score <= 100


def test_parse_txt_bullets():
    raw = b"- Led migration to FastAPI\n- Reduced latency by 40%\nSome prose here.\n"
    parsed = parse(raw, "resume.txt")
    assert isinstance(parsed, ParsedResume)
    assert "Led migration to FastAPI" in parsed.bullets
    assert "Reduced latency by 40%" in parsed.bullets


def test_strip_pii():
    text = "Reach me at jane@example.com or +1 (555) 123-4567, site https://jane.dev"
    cleaned = strip_pii(text)
    assert "jane@example.com" not in cleaned
    assert "[email]" in cleaned
    assert "[phone]" in cleaned
    assert "[url]" in cleaned


def test_jd_extract():
    jd = "Senior Software Engineer with 6+ years of Python, React and Kubernetes."
    out = jd_extractor.extract(jd)
    assert "python" in out.skills
    assert "kubernetes" in out.skills
    assert out.years_experience == 6
    assert "senior software engineer" in out.titles
