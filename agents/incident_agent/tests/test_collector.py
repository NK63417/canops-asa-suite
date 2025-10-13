from agents.incident_agent.collector.io import read_lines, head
from pathlib import Path

def test_head_returns_first_lines():
    p = Path("data/logs/app.log")
    lines = head(str(p), n=2)
    assert len(lines) == 2
    assert lines[0].startswith("[2025-08-01T12:00:00Z] ERROR")
    assert "Retry scheduled" in lines[1]

def test_read_lines_streams_all():
    p = Path("data/logs/app.log")
    all_lines = list(read_lines(str(p)))
    assert len(all_lines) >= 4
    assert any("EXCEPTION" in l for l in all_lines)