"""
AuditFlow CLI — the easiest on-ramp.

Commands:
  plan          What do I need for this goal?
  self-audit    Does the control plane hold?
  run           End-to-end: ingest → validate → roll-forward → workpaper
  serve         Start the API

Usage:
  python -m app.cli plan
  python -m app.cli self-audit
  python -m app.cli run
  python -m app.cli run --prior my_2025.xlsx --current my_2026.xlsx
  python -m app.cli serve
"""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import sys
from pathlib import Path

os.environ.setdefault("DATABASE_URL", "sqlite+aiosqlite:////tmp/aflo.db")


def cmd_plan(args: argparse.Namespace) -> int:
    from app.services.intake_planner import Goal, plan_for_goal, print_plan

    goal = Goal(args.goal)
    prior = Path(args.prior) if args.prior else None
    current = Path(args.current) if args.current else None
    plan = plan_for_goal(goal, prior_path=prior, current_path=current)
    print_plan(plan)
    if args.json:
        print(json.dumps(plan.to_dict(), indent=2))
    return 0


def cmd_self_audit(args: argparse.Namespace) -> int:
    from app.services.self_audit import print_report, run_self_audit

    report = run_self_audit()
    print_report(report)
    out = Path(args.output or "output/self_audit_report.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report.to_dict(), indent=2))
    print(f"\nReport written → {out}")
    return 0 if report.score >= 80 else 1


def cmd_run(args: argparse.Namespace) -> int:
    from app.demo import run_demo

    print("Launching governed pipeline…")
    print("(Using synthetic data if no custom workbooks provided.)")
    print()
    asyncio.run(run_demo())
    return 0


def cmd_serve(args: argparse.Namespace) -> int:
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=args.host,
        port=args.port,
        reload=args.reload,
    )
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="aflo",
        description=(
            "AuditFlow — Governed AI Workpaper Automation\n"
            "The model proposes. The governed system validates.\n"
            "The evidence establishes provenance. The authorized human establishes final authority."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = p.add_subparsers(dest="command", required=True)

    plan = sub.add_parser("plan", help="Discern what is needed for a goal")
    plan.add_argument(
        "--goal",
        default="rollforward_workpaper",
        choices=["rollforward_workpaper", "self_audit", "ingest_only", "verify_facts"],
    )
    plan.add_argument("--prior", help="Path to prior-year workbook")
    plan.add_argument("--current", help="Path to current-year workbook")
    plan.add_argument("--json", action="store_true", help="Also emit machine-readable plan")
    plan.set_defaults(func=cmd_plan)

    audit = sub.add_parser("self-audit", help="Inspect the control plane and emit a capability report")
    audit.add_argument("--output", "-o", help="JSON report path")
    audit.set_defaults(func=cmd_self_audit)

    run = sub.add_parser("run", help="Execute end-to-end governed pipeline")
    run.add_argument("--prior", help="Prior-year Excel (optional; synthetic used if omitted)")
    run.add_argument("--current", help="Current-year Excel (optional)")
    run.set_defaults(func=cmd_run)

    serve = sub.add_parser("serve", help="Start FastAPI server")
    serve.add_argument("--host", default="127.0.0.1")
    serve.add_argument("--port", type=int, default=8000)
    serve.add_argument("--reload", action="store_true")
    serve.set_defaults(func=cmd_serve)

    return p


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
