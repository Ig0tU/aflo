"""
AuditFlow FastAPI application.

The model is not the system of record.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import __version__
from app.api.router import router
from app.db.session import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(
    title="AuditFlow",
    description=(
        "Governed AI Workpaper Automation — "
        "The model proposes. The governed system validates. "
        "The evidence establishes provenance. The authorized human establishes final authority."
    ),
    version=__version__,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.get("/")
async def root():
    return {
        "name": "AuditFlow",
        "version": __version__,
        "principle": (
            "The model proposes. The governed system validates. "
            "The evidence establishes provenance. The authorized human establishes final authority."
        ),
        "docs": "/docs",
    }


@app.get("/health")
async def health():
    return {"status": "ok"}
