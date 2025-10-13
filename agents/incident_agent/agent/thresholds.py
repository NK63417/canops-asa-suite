# agents/incident_agent/agent/thresholds.py
from __future__ import annotations
import json, uuid, yaml
from datetime import datetime, timezone
from pathlib import Path

def load_thresholds(path: str = "config.yaml") -> dict[str, int]:
    if not Path(path).exists():
        return {}
    with open(path, "r") as f:
        data = yaml.safe_load(f) or {}
    t = data.get("thresholds", {}) or {}
    # coerce to ints when possible
    return {k: int(v) for k, v in t.items() if v is not None}

def decide_incident(counts: dict[str, int], thresholds: dict[str, int]) -> dict | None:
    breaches = []
    for sev, cnt in counts.items():
        thr = thresholds.get(sev)
        if thr is None:
            continue
        if cnt >= thr:
            breaches.append((sev, cnt))
    if not breaches:
        return None
    return {
        "incident_id": str(uuid.uuid4()),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "breaches": [{"sev": s, "count": c} for s, c in breaches],
        "status": "OPEN",
    }

def record_incident(payload: dict, path: str = "outputs/incidents.jsonl") -> None:
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("a") as f:
        f.write(json.dumps(payload) + "\n")