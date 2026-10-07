# Interview Talking Points — AuditFlow

## One-sentence positioning

I build governed agentic systems: LLMs perform extraction, classification and reasoning while deterministic services retain control of validation, provenance, authorization, state and final outputs.

## Core phrase (repeat it)

> The model is not the system of record.

Expand:

> The model produces structured proposals. The application validates them. The database establishes authoritative state. The workflow determines what can happen. And the human retains authority where the consequence requires it.

## STAR story for “Tell me about a system where AI interacted with real business data”

**Problem**  
The information needed to make a decision existed across multiple systems and files that didn’t share enough context.

**Failure mode**  
A naïve AI implementation could retrieve information and produce a plausible answer, but there was no guarantee that the answer represented authoritative data.

**Architecture**  
I separated perception from decision and authority. Agents could extract and reason, but deterministic services controlled what entered the authoritative data layer.

**Provenance**  
Every important value needed source context and a state indicating whether it was observed, inferred, stale, conflicting, or verified.

**Human control**  
The system could recommend an action, but the appropriate human retained authority over consequential changes.

**Result**  
That allowed automation to be introduced incrementally rather than replacing a manual process all at once.

## Mapping to the role’s language

| Their need | AuditFlow demonstration |
|---|---|
| Intelligent document intake | Excel/XLSM sensing with cell provenance |
| Structured records from client files | Pydantic + SQLAlchemy facts with domain keys |
| Prior-year → current-year roll-forward | Explicit reconciliation deltas + material change detection |
| Human review of exceptions | Verify / reject endpoints + immutable AuditEvent ledger |
| Governed data layer | VerificationStatus lifecycle, never model-as-SOR |
| Reproducible workpapers | openpyxl renderer with live variance formulas |

## What to de-emphasize

- Cryptocurrency / gaming / speculative AGI language
- “I built MeshOS” without translation
- Claims of fully autonomous agents replacing humans
- Hobby-project framing

## What to emphasize

- Control plane around AI
- Provenance and auditability
- Deterministic boundaries around probabilistic models
- Human-in-the-loop as first-class design, not afterthought
- Incremental introduction of automation
