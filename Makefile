.PHONY: dev backend frontend test

dev:
	docker compose up --build

backend:
	cd backend && uvicorn app.main:app --reload

frontend:
	cd frontend && pnpm dev

test:
	cd backend && pytest -q
