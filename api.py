"""
api.py
------
FastAPI server that exposes the LangGraph review pipeline
as a REST API for the frontend to consume.

Run with:
  pip install fastapi uvicorn
  uvicorn api:app --reload --port 8000
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

from graph.review_graph import review_graph
from graph.state import CodeReviewState
from config.settings import MAX_CODE_LENGTH

app = FastAPI(title="CodeScan API", version="1.0.0")

# ── CORS — allows the HTML frontend to call this API ──────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Serve static frontend files ────────────────────────────────────────
app.mount("/static", StaticFiles(directory="static"), name="static")


# ── Request / Response schemas ─────────────────────────────────────────
class ReviewRequest(BaseModel):
    code: str
    language: Optional[str] = "auto"


class ReviewResponse(BaseModel):
    language: str
    score: int
    total_issues: int
    style_issues: list
    bug_issues: list
    security_issues: list
    fix_suggestions: str
    final_report: str


# ── Routes ─────────────────────────────────────────────────────────────
@app.get("/")
def serve_frontend():
    """Serve the HTML frontend."""
    return FileResponse("static/index.html")


@app.post("/review", response_model=ReviewResponse)
def run_review(req: ReviewRequest):
    """
    Main endpoint — receives code, runs LangGraph pipeline,
    returns structured review results.
    """
    code = req.code.strip()

    if not code:
        raise HTTPException(status_code=400, detail="No code provided.")

    if len(code) > MAX_CODE_LENGTH:
        code = code[:MAX_CODE_LENGTH]

    # Build initial state
    initial_state: CodeReviewState = {
        "raw_code":         code,
        "language":         "" if req.language == "auto" else req.language,
        "style_issues":     [],
        "bug_issues":       [],
        "security_issues":  [],
        "fix_suggestions":  "",
        "final_report":     "",
        "error":            None,
    }

    try:
        result = review_graph.invoke(initial_state)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    style    = result.get("style_issues", [])
    bugs     = result.get("bug_issues", [])
    security = result.get("security_issues", [])
    all_issues = style + bugs + security

    # Calculate score
    counts = {"CRITICAL":0,"HIGH":0,"MEDIUM":0,"LOW":0,"INFO":0}
    for issue in all_issues:
        sev = (issue.get("severity","INFO") or "INFO").upper()
        if sev in counts:
            counts[sev] += 1

    penalty = counts["CRITICAL"]*25 + counts["HIGH"]*15 + counts["MEDIUM"]*7 + counts["LOW"]*2
    score = max(0, 100 - penalty)

    return ReviewResponse(
        language        = result.get("language", "unknown"),
        score           = score,
        total_issues    = len(all_issues),
        style_issues    = style,
        bug_issues      = bugs,
        security_issues = security,
        fix_suggestions = result.get("fix_suggestions", ""),
        final_report    = result.get("final_report", ""),
    )


@app.get("/health")
def health():
    return {"status": "ok", "service": "CodeScan API"}