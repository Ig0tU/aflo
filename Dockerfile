# AuditFlow — governed workpaper automation
# Default: SQLite, no external services required.
# Build:  docker build -t aflo .
# Run:    docker run --rm -p 8000:8000 -v "$(pwd)/output:/app/output" aflo

FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app \
    DATABASE_URL=sqlite+aiosqlite:////app/data/aflo.db \
    APP_ENV=production

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ app/
COPY data/ data/
COPY alembic/ alembic/
COPY alembic.ini .
COPY docs/ docs/
COPY tests/ tests/

RUN mkdir -p /app/output /app/data

COPY docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

EXPOSE 8000
ENTRYPOINT ["/docker-entrypoint.sh"]
