# 🧠 CanOps ASA Suite
**Canadian Operations Application Support Analyst Suite**

A simulated **incident management toolkit** inspired by real-world ASA (Application Support Analyst) workflows in Canadian enterprise environments (RBC, TD, CGI, etc.).  
This suite automates **log parsing, severity classification, incident window analysis, and SLA reporting** — bridging the gap between traditional IT support and Python-based automation.

---

## 🚀 Live Mission
**Objective:**  
Demonstrate end-to-end ASA capabilities through automation:
- Parse and triage application logs.  
- Classify incidents (SEV1–SEV4) by severity.  
- Summarize health metrics from live logs.  
- Simulate ServiceNow-style incident workflows.

---

## 🧩 Architecture Overview
canops-asa-suite/
├── agents/
│   └── incident_agent/
│       ├── collector/
│       │   └── io.py                 # Reads and streams log data
│       ├── analyzer/
│       │   └── classify.py           # Classifies incidents by severity
│       └── tests/
│           ├── test_collector.py     # Unit tests for log reader
│           ├── test_analyzer.py      # Unit tests for classifier logic
│           └── test_smoke.py         # Sanity checks
├── data/
│   └── logs/app.log                  # Sample log data
├── pytest.ini
└── README.md

---


🧰 Tech Stack

Tool
Purpose
Python 3.11+
Core language
Pytest
Testing framework
SQLite (Planned)
Simulated incident DB
Pandas (Planned)
SLA analysis and reporting
VS Code + GitHub
Development + version control
