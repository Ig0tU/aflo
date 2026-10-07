# AuditFlow — local shortcuts (no Docker required)

.PHONY: audit plan run demo serve test docker

audit:
	PYTHONPATH=. python -m app.cli self-audit

plan:
	PYTHONPATH=. python -m app.cli plan

run:
	PYTHONPATH=. python -m app.cli run

demo: audit run

serve:
	PYTHONPATH=. python -m app.cli serve

test:
	PYTHONPATH=. python -m pytest tests/ -q

docker:
	docker compose up --build
