# agents/incident_agent/cli.py
from __future__ import annotations
import argparse
from agents.incident_agent.collector.io import read_lines
from agents.incident_agent.analyzer.classify import window_counts
from agents.incident_agent.agent.thresholds import (
    load_thresholds, decide_incident, record_incident
)

def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="Incident summary (last N seconds)")
    p.add_argument("log", help="path to log file")
    p.add_argument("--window", type=int, default=60, help="window seconds")
    p.add_argument("--config", default="config.yaml", help="thresholds yaml")
    p.add_argument("--out", default="outputs/incidents.jsonl", help="sink jsonl")
    p.add_argument("--notify", action="store_true", help="send mock Slack alert")
    p.add_argument("--channel", default="#incidents", help="mock Slack channel") 
    args = p.parse_args(argv)

    lines = list(read_lines(args.log))
    counts, samples = window_counts(lines, window_sec=args.window)

    print(f"=== Incident Summary (Last {args.window}s) ===")
    for k in ("SEV1","SEV2","SEV3","SEV4","INFO"):
        if k in counts:
            print(f"{k}: {counts[k]}")
    print("-" * 35)
    for s in samples:
        print(f"- {s}")

    thresholds = load_thresholds(args.config)
    incident = decide_incident(counts, thresholds)
    if incident:
        record_incident(incident, path=args.out)
        if args.notify:
            from agents.incident_agent.notifier.slack import notify
            notify(incident, args.channel)
        print(f"\n🚨 Incident recorded: {incident['incident_id']} → {args.out}")
    else:
        print("\nNo threshold breaches detected.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())