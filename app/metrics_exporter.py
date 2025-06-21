
"""Prometheus exporter exposing audit‑log metrics."""
from fastapi import APIRouter, Response
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST

memory_violations = Counter(
    "memory_diff_violations_total",
    "Number of untracked memories detected by diff‐audit"
)
slot_clears = Counter(
    "slot_clears_total",
    "Number of slots cleared by slot_scrubber"
)

router = APIRouter()

@router.get("/metrics")
def metrics():
    data = generate_latest()
    return Response(content=data, media_type=CONTENT_TYPE_LATEST)
