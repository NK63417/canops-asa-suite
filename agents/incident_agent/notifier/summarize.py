from __future__ import annotations
from pathlib import Path
import json
from datetime import datetime

def summarize(jsonl_path: str = "outputs/incidents.jsonl",
              out_md: str = "outputs/incidents.md") -> str:
    p = Path(jsonl_path)
    if not p.exists():
        return ""

    lines = [json.loads(x) for x in p.read_text().splitlines() if x.strip()]
    if not lines:
        return ""

    lines.sort(key=lambda r: r.get("timestamp",""))
    total = len(lines)
    last = lines[-1]
    sev_counts = {}
    for r in lines:
        for b in r.get("breaches", []):
            sev_counts[b["sev"]] = sev_counts.get(b["sev"], 0) + 1

    md = []
    md.append("# Incident Summary\n")
    md.append(f"- Generated: {datetime.utcnow().isoformat()}Z")
    md.append(f"- Total incidents: {total}\n")
    md.append("## Breach counts by SEV")
    for sev in ("SEV1","SEV2","SEV3","SEV4"):
        if sev in sev_counts:
            md.append(f"- {sev}: {sev_counts[sev]}")
    md.append("\n## Last incident")
    md.append(f"- id: `{last['incident_id']}`")
    md.append(f"- time: {last['timestamp']}")
    md.append(f"- breaches: {[b['sev']+':'+str(b['count']) for b in last.get('breaches',[])]}")
    if "db_health" in last:
        dh = last["db_health"]
        md.append(f"- db_health: connect={dh.get('can_connect')} "
                  f"orders_table={dh.get('orders_table_exists')} "
                  f"rowcount={dh.get('orders_rowcount')}")
    md.append("\n## All incidents (latest first)")
    for r in reversed(lines):
        md.append(f"- {r['timestamp']} | {r['incident_id']} | "
                  f"{','.join(b['sev'] for b in r.get('breaches',[]))}")
    Path(out_md).write_text("\n".join(md))
    return out_md