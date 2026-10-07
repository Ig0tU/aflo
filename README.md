# AuditFlow

**Governed AI Workpaper Automation**

> The model proposes. The governed system validates. The evidence establishes provenance. The authorized human establishes final authority.

AuditFlow is a reference architecture for high-stakes operational automation. It demonstrates how to combine LLM-assisted extraction and reasoning with deterministic validation, full provenance, human-in-the-loop authority, and reproducible workpaper generation — without treating the model as the system of record.

This prototype was purpose-built around the requirements of governed audit / employee-benefit workpaper automation workflows.

---

## Why this exists

Most AI demos stop at “the model produced an answer.”

In regulated or high-stakes domains that is insufficient. You need:

- Source-level provenance on every extracted value
- Explicit verification state (observed → proposed → validated → human-authorized)
- Deterministic policy boundaries around probabilistic model output
- Historical roll-forward comparison with change detection
- Immutable audit events
- Human authority retained for consequential actions
- Reproducible Excel / Word workpapers that carry the evidence trail

AuditFlow implements that control plane.

---

## Architecture

```
Client Documents (Excel / XLSM)
        │
        ▼
┌───────────────────────┐
│  Document Intake      │  openpyxl extraction
│  + Structured Sensing │  cell-level coordinates preserved
└───────────┬───────────┘
            │
            ▼
┌───────────────────────┐
│  Pydantic Domain      │  typed records + provenance fields
│  Models               │
└───────────┬───────────┘
            │
            ▼
┌───────────────────────┐
│  Deterministic        │  confidence thresholds, invariants,
│  Validation Layer     │  conflict / staleness rules
└───────────┬───────────┘
            │
            ▼
┌───────────────────────┐
│  PostgreSQL           │  authoritative state
│  (SQLAlchemy/Alembic) │  audit_cycles, extracted_facts,
└───────────┬───────────┘  reconciliation_deltas, audit_events
            │
     ┌──────┼──────┐
     ▼      ▼      ▼
 Roll-forward   Exceptions   AI Follow-ups
 Comparison     Flagging     (structured proposals)
     │      │      │
     └──────┼──────┘
            ▼
┌───────────────────────┐
│  Human Review Surface │  verify / reject / route
└───────────┬───────────┘
            │
            ▼
┌───────────────────────┐
│  Workpaper Renderer   │  publication-grade Excel
│  (openpyxl)           │  with variance formulas & evidence
└───────────────────────┘
```

**Core invariant:** The LLM never writes directly to authoritative state. It produces structured proposals that pass through validation and human authority gates.

---

## Key capabilities demonstrated

| Capability | Implementation |
|---|---|
| Intelligent document intake | Excel/XLSM sensing with cell provenance (`Participants!D2`) |
| Structured records | Pydantic models carrying value + source + location + author + confidence + verification_status |
| Provenance & auditability | Immutable `AuditEvent` ledger per fact |
| Historical roll-forward | Prior-year ↔ current-year comparison with delta classification |
| Deterministic validation | Auto-validation policy engine with confidence + invariant thresholds |
| Human-in-the-loop | Explicit verify / reject / flag endpoints with mandatory rationale |
| Workpaper generation | openpyxl renderer producing formatted roll-forward sheets with Excel formulas |
| Governance vocabulary | VerificationStatus, DeltaType, FactType enums that map cleanly to enterprise audit language |

---

## Quick start

```bash
# Clone
git clone https://github.com/Ig0tU/aflo.git
cd aflo

# Optional: use Docker for PostgreSQL
docker compose up -d

# Install
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Environment
cp .env.example .env
# Edit DATABASE_URL if needed

# Run the end-to-end demo (creates synthetic data + workpaper)
python -m app.demo

# API
uvicorn app.main:app --reload
# Open http://localhost:8000/docs
```

Without Docker the demo falls back to SQLite so you can explore immediately.

---

## Project layout

```
aflo/
├── app/
│   ├── main.py                 # FastAPI entry
│   ├── api/                    # routers (cycles, facts, verification)
│   ├── core/                   # config, security boundaries
│   ├── models/                 # SQLAlchemy + Pydantic domain models
│   ├── services/               # extraction, validation, rollforward, renderer
│   └── db/                     # session, base
├── alembic/                    # migrations
├── data/synthetic/             # sample prior/current year workbooks
├── tests/
├── docs/                       # architecture notes + interview talking points
├── docker-compose.yml
└── README.md
```

---

## Interview narrative (ready to use)

**Problem**  
The information needed to make a decision existed across multiple systems and files that did not share enough context.

**Failure mode**  
A naïve AI implementation could retrieve information and produce a plausible answer, but there was no guarantee the answer represented authoritative data.

**Architecture**  
I separated perception from decision and authority. Agents / extractors can observe and propose. Deterministic services control what enters the authoritative data layer.

**Provenance**  
Every important value carries source context and a state indicating whether it is observed, inferred, stale, conflicting, or verified.

**Human control**  
The system can recommend an action; the appropriate human retains authority over consequential changes.

**Result**  
Automation can be introduced incrementally rather than replacing a manual process all at once.

**Theme line**  
> The model is not the system of record.

---

## Design principles visible in the code

1. **Capability-based boundaries** — extraction, validation, reconciliation, and rendering are distinct services.
2. **Provenance first** — no value without source + location + author + timestamp + verification status.
3. **Deterministic gates around probabilistic output** — confidence thresholds and invariant checks run before any auto-transition.
4. **Immutable event history** — every status change is an `AuditEvent`.
5. **Human authority is explicit** — verification endpoints require actor_id + reason.
6. **Reproducible outputs** — workpapers are generated from the governed state, not from ephemeral model responses.

---

## What this is (and is not)

- ✅ A synthetic, interview-grade reference implementation of governed AI workpaper automation
- ✅ A concrete demonstration of the control-plane architecture many audit / operational AI roles require
- ✅ Fully runnable locally (SQLite fallback) or with PostgreSQL
- ❌ Not a production audit platform
- ❌ Not trained on or containing any real client data
- ❌ Not claiming to replace professional judgment

---

## License

MIT — use, adapt, or reference freely for portfolio and interview purposes.
