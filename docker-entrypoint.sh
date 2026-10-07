#!/bin/sh
set -e
cd /app

mkdir -p /app/data /app/output

echo "────────────────────────────────────────"
echo " AuditFlow"
echo " The model is not the system of record."
echo "────────────────────────────────────────"

python -m app.cli self-audit || true
echo ""

if [ "${AFLO_RUN_DEMO:-1}" = "1" ]; then
  echo "Running governed pipeline (synthetic data)…"
  python -m app.cli run || true
  echo ""
fi

echo "API: http://0.0.0.0:8000/docs"
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
