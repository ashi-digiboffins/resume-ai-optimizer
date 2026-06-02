# Resume AI Optimizer

> Paste a job description, upload your resume, get a tailored rewrite + ATS keyword diff + match score. **Next.js 15 + FastAPI + Anthropic Claude**.

![Stack](https://img.shields.io/badge/stack-Next.js%20%2B%20FastAPI%20%2B%20Claude-orange) ![Python](https://img.shields.io/badge/python-3.11-yellow) ![License](https://img.shields.io/badge/license-MIT-green)

## Why

Most "AI resume" tools just rewrite the whole CV and lose your voice. This one runs three focused passes:

1. **Extract** — pull skills, titles, and years-of-experience from the JD.
2. **Score** — measure ATS keyword coverage (the JD's weighted vocabulary vs. your resume).
3. **Rewrite** — bullet-by-bullet, preserving your phrasing, with a `strictness` slider for how aggressive the rewrite is.

It never invents experience you don't have — the system prompt enforces that (no fabricated employers, years, titles, or technologies).

## Features

- DOCX / PDF / TXT resume parsing with bullet extraction (`pdfplumber`, `python-docx`)
- Dependency-free ATS keyword coverage scoring (weighted by JD term frequency)
- Hallucination-guarded, bullet-by-bullet rewrites via Claude
- Heuristic JD extractor — skills, titles, years (no LLM call needed)
- **Anonymous mode** — strips emails / phones / URLs before sending to the LLM
- Export tailored bullets back to a `.docx`
- Side-by-side redline diff view + ATS score panel in the UI

## Architecture

```
Next.js 15 ──► FastAPI /api/analyze ──► parser  (resume → text + bullets)
                                    ├─► ats_score (JD vs resume → score + diff)
                                    └─► rewriter  (Claude, hallucination-guarded)
                  /api/extract  ──► jd_extractor (skills / titles / years)
                  /api/export   ──► python-docx  (bullets → .docx download)
```

## Tech stack

| Layer | Choice |
|---|---|
| Frontend | Next.js 15 (App Router), React 18, Tailwind CSS |
| Backend | FastAPI, Pydantic v2 |
| LLM | Anthropic Claude (`claude-sonnet-4-6`), lazily initialised |
| Parsing | `pdfplumber`, `python-docx` |

## Quick start

```bash
make dev          # docker compose up --build  (API :8000, web :3000)
```

Local dev:

```bash
# backend
cd backend
python3.11 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env          # add ANTHROPIC_API_KEY
uvicorn app.main:app --reload

# frontend
cd ../frontend && npm install && npm run dev
```

> The ATS score and JD extraction work without any API key; only the bullet **rewrite** step calls Claude.

## Configuration

Backend env (`backend/.env`):

| Variable | Default | Purpose |
|---|---|---|
| `ANTHROPIC_API_KEY` | _(empty)_ | Required for rewrites |
| `OPENAI_API_KEY` | _(empty)_ | Optional alternate provider |
| `CORS_ORIGINS` | `http://localhost:3000` | Allowed origins |

Frontend: `NEXT_PUBLIC_API_URL` (default `http://localhost:8000`).

## API reference

| Method | Path | Body | Description |
|---|---|---|---|
| `GET` | `/health` | — | Liveness + version |
| `POST` | `/api/analyze` | multipart: `resume`, `job_description`, `strictness` | Full pass: ATS score + keyword diff + rewrites |
| `POST` | `/api/rewrite` | `{bullets, job_description, strictness}` | Rewrite bullets only |
| `POST` | `/api/extract` | query `job_description` | Skills / titles / years from a JD |
| `POST` | `/api/export` | `{name, bullets}` | Download tailored bullets as `.docx` |

## Project structure

```
backend/
  app/
    main.py
    schemas.py                # shared pydantic models
    api/
      analyze.py              # score + rewrite in one call
      rewrite.py              # standalone rewrite + JD extract
      export.py               # bullets → .docx
    services/
      parser.py               # resume → plaintext + bullets, strip_pii
      ats_score.py            # keyword coverage scoring
      jd_extractor.py         # heuristic skills/titles/years
      rewriter.py             # Claude rewrite (lazy client)
  tests/                      # services + endpoints
  requirements.txt
  Dockerfile
frontend/
  app/page.tsx                # uploader + JD + results
  components/
    ResumeUploader.tsx  JDInput.tsx  ScorePanel.tsx  DiffView.tsx
  lib/api.ts
docker-compose.yml
Makefile
```

## Testing

```bash
cd backend && pip install -r requirements.txt && pip install pytest ruff httpx
pytest -q          # ats scoring, parser, PII scrub, JD extract, endpoints
ruff check app tests
```

## Deployment

- **Backend**: `backend/Dockerfile` → Fly.io/Render; set `ANTHROPIC_API_KEY`.
- **Frontend**: `npm run build` → Vercel; set `NEXT_PUBLIC_API_URL`.

## Roadmap

- [ ] Cover letter generator
- [ ] Multi-language support
- [ ] Browser extension (right-click a JD on LinkedIn)

## License

MIT — see [LICENSE](LICENSE).
