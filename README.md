# AuditFlow

**Governed AI Workpaper Automation**

> The model proposes. The governed system validates. The evidence establishes provenance. The authorized human establishes final authority.

AuditFlow is a reference architecture for high-stakes operational automation. It shows how to combine extraction and reasoning with deterministic validation, full provenance, human-in-the-loop authority, and reproducible workpapers — without treating the model as the system of record.

Built as an interview-grade prototype for governed audit / employee-benefit workpaper workflows. Synthetic data only. No client information.

---

## One-command paths

### Local (no Docker)

```bash
pip install -r requirements.txt
make demo          # self-audit + full pipeline → output/rollforward_workpaper.xlsx
```

Or step by step:

```bash
make audit         # control-plane self-check (target: 100/100)
make plan          # what inputs are needed for a roll-forward workpaper
make run           # ingest → validate → roll-forward → workpaper
make serve         # API at http://127.0.0.1:8000/docs
```

### Docker

```bash
docker compose up --build
```

- API: http://localhost:8000/docs
- Workpaper written to `./output/`
- Uses SQLite inside the container (no Postgres required)
- Optional Postgres: `docker compose --profile postgres up --build`

There is no hardware auto-detection and no claim of production readiness. One container, one volume mount, one API.

---

## What it demonstrates

| Concern | How |
|--------|-----|
| Document intake | Excel/XLSM with **cell-level provenance** (`Participants!D2`) |
| Structured records | Pydantic + SQLAlchemy facts with domain keys and verification state |
| Deterministic boundary | Policy engine; never elevates to `HUMAN_VERIFIED` |
| Roll-forward | Prior-year ↔ current-year comparison + material-change classification |
| Human authority | Verify/reject endpoints require `actor_id` + reason; every change is an `AuditEvent` |
| Reproducible output | openpyxl workpaper with variance formulas and evidence columns |
| Self-inspection | `make audit` / `python -m app.cli self-audit` scores the control plane |

**Core invariant:** the model never writes authoritative state. It can propose; validation and humans decide.

---

## Architecture (short)

```
Excel sources
    → extraction (source + cell + author + confidence)
    → deterministic validation
    → PostgreSQL or SQLite (authoritative state)
    → roll-forward / exceptions
    → human review (explicit)
    → workpaper (Excel)
```

Self-audit checks that this boundary holds (provenance schema, verification lifecycle, policy never grants human authority, tests pass).

---

## Bring your own data (honest path)

1. Place prior- and current-year workbooks somewhere reachable.
2. Today the domain map is the built-in demo map (`Participants!D2`, etc.). Custom sheet/cell maps are a natural extension; they are not pretended to exist yet.
3. Run:

```bash
PYTHONPATH=. python -m app.cli plan
PYTHONPATH=. python -m app.cli run
```

Synthetic employee-benefit workbooks under `data/synthetic/` are used when you do not supply files, so the pipeline is always demonstrable.

---

## Project layout

```
app/
  cli.py              # plan | self-audit | run | serve
  main.py             # FastAPI
  api/                # verification, auto-validate, roll-forward
  models/             # domain + ORM (provenance-first)
  services/           # extraction, validation, rollforward, renderer, self_audit, intake_planner
data/synthetic/       # demo prior/current year workbooks
docs/                 # interview talking points
tests/
Dockerfile
docker-compose.yml
Makefile
```

---

## Interview line

> The model is not the system of record.
> It produces structured proposals. The application validates them. The database holds authoritative state. The workflow decides what can happen. The authorized human retains authority where consequence requires it.

STAR-style story and role mapping: `docs/INTERVIEW_TALKING_POINTS.md`.

---

## What this is not

- Not a production audit platform
- Not trained on or containing real client data
- Not autonomous agents replacing professional judgment
- Not hardware-sensing or self-configuring infrastructure

It is a clear, runnable demonstration of the control plane this class of role is hired to build.

---

## License

MIT — use and adapt for portfolio and interview purposes.
