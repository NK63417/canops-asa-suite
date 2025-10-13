from agents.incident_agent.analyzer.classify import classify, parse_ts, window_counts

LINES = [
    "[2025-08-01T12:00:00Z] ERROR Payment failed for order 12345",
    "[2025-08-01T12:00:30Z] WARN Retry scheduled in 30s",
    "[2025-08-01T12:01:00Z] EXCEPTION NullReference at /payments/charge",
    "[2025-08-01T12:01:30Z] INFO Background job started",
]

def test_classify_rules():
    assert classify("FATAL boom") == "SEV1"
    assert classify("Unhandled EXCEPTION") == "SEV1"
    assert classify("ERROR x") == "SEV2"
    assert classify("failed to connect") == "SEV2"
    assert classify("timeout waiting") == "SEV3"
    assert classify("WARNING: heads up") == "SEV4"
    assert classify("all good") == "INFO"

def test_parse_ts_iso():
    ts = parse_ts(LINES[0])
    assert ts is not None and ts.isoformat().endswith("+00:00")

def test_window_counts_last_minute():
    counts, samples = window_counts(LINES, window_sec=60)
    # newest is 12:01:30 → window includes 12:00:30..12:01:30
    # includes: WARN (SEV4), EXCEPTION (SEV1), INFO
    assert counts.get("SEV1", 0) == 1
    assert counts.get("SEV3", 0) == 1
    # ensure sample captured the severe line
    assert any(s.startswith("SEV1:") for s in samples)