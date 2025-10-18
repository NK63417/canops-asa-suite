# agents/incident_agent/store/health.py
from __future__ import annotations
import sqlite3
from typing import Dict

def snapshot(db_path: str = "data/db/canops.db") -> Dict[str, str]:
    out = {"can_connect": "FAIL", "orders_table_exists": "FAIL", "orders_rowcount": "0"}
    try:
        con = sqlite3.connect(db_path)
        out["can_connect"] = "PASS"
        cur = con.cursor()
        cur.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name='orders'")
        out["orders_table_exists"] = "PASS" if cur.fetchone() else "FAIL"
        cur.execute("SELECT COUNT(*) FROM orders")
        out["orders_rowcount"] = str(cur.fetchone()[0])
        con.close()
    except Exception as e:
        out["error"] = str(e)
    return out