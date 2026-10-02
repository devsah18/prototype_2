from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from analytics import calculate_metrics
from database import (
    get_entities,
    get_relationships,
    initialize_database
)
from graph import graph_for_frontend
from models import TextAnalysisRequest
from nlp import extract_entities


BASE_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = BASE_DIR.parent / "frontend"


app = FastAPI(
    title="AI Criminal Network Analysis System",
    version="1.0.0",
    description=(
        "Prototype system for entity and relationship "
        "network analysis using fictional demo data."
    )
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.on_event("startup")
def startup():
    initialize_database()


@app.get("/")
def home():
    return FileResponse(
        FRONTEND_DIR / "index.html"
    )


@app.get("/api/entities")
def entities():
    return get_entities()


@app.get("/api/relationships")
def relationships():
    return get_relationships()


@app.get("/api/graph")
def graph():
    return graph_for_frontend()


@app.get("/api/analytics")
def analytics():
    return calculate_metrics()


@app.post("/api/analyze-text")
def analyze_text(request: TextAnalysisRequest):
    return extract_entities(request.text)


@app.get("/api/health")
def health():
    return {
        "status": "ok",
        "system": "AI Criminal Network Analysis System"
    }
