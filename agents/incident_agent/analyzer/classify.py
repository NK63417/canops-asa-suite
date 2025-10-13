# agents/incident_agent/analyzer/classify.py
from __future__ import annotations
import re
from datetime import datetime, timezone, timedelta
from typing import Iterable, Tuple, Dict, List

# Regex → SEV mapping (order matters)
RULES: list[tuple[str, str]] = [
    (r"\b(exception|traceback|fatal)\b", "SEV1"),
    (r"\b(error|failed|panic)\b",        "SEV2"),
    (r"\b(timeout|retry|degraded)\b",    "SEV3"),
    (r"\b(warn|warning)\b",              "SEV4"),
]

TS_RX = re.compile(r"\[(.*?)\]\s*(.*)")

def parse_ts(line: str) -> datetime | None:
    """
    Parse ISO-8601 timestamp in square brackets: [2025-08-01T12:00:00Z]
    Returns aware UTC datetime, or None if not found.
    """
    m = TS_RX.match(line)
    if not m:
        return None
    ts = m.group(1).replace("Z", "+00:00")
    try:
        return datetime.fromisoformat(ts).astimezone(timezone.utc)
    except Exception:
        return None

def classify(line: str) -> str:
    """
    Map a log line to INFO/SEV4/SEV3/SEV2/SEV1 based on keywords.
    """
    low = line.lower()
    for pat, sev in RULES:
        if re.search(pat, low):
            return sev
    return "INFO"

def window_counts(lines: Iterable[str], window_sec: int = 60) -> Tuple[Dict[str, int], List[str]]:
    """
    Count SEVs in the last `window_sec` seconds relative to the newest timestamp in `lines`.
    Returns (counts_by_sev, samples) where samples are up to 3 SEV1/SEV2 messages.
    """
    parsed: list[tuple[datetime | None, str, str]] = []
    newest: datetime | None = None

    for ln in lines:
        ts = parse_ts(ln)
        sev = classify(ln)
        parsed.append((ts, ln, sev))
        if ts and (newest is None or ts > newest):
            newest = ts

    if newest is None:
        return {}, []

    cutoff = newest - timedelta(seconds=window_sec)
    counts: Dict[str, int] = {}
    samples: List[str] = []

    for ts, ln, sev in parsed:
        if ts and ts >= cutoff:
            counts[sev] = counts.get(sev, 0) + 1
            if sev in ("SEV1", "SEV2") and len(samples) < 3:
                # Trim timestamp for readability
                msg = TS_RX.match(ln).group(2) if TS_RX.match(ln) else ln
                samples.append(f"{sev}: {msg}")

    return counts, samples