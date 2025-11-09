---
title: Metrics & Golden Tests
version: "0.1"
date: 2025-10-03
status: draft
---

# ProdOS LLM Metrics and Golden Tests

This folder defines how we measure, log, and validate the quality of the ProdOS LLM multi‑agent system. It complements `product/llm-framework-enhancements.md`.

---

## Directory Layout

```
.agent-os/metrics/
├── README.md                   # This file
├── decision-logs/              # JSONL logs (one event per line)
├── golden/                     # Scenario fixtures and assertions
│   ├── README.md               # How to use golden tests
│   ├── low-energy-15m.json
│   ├── big-rock-due-tomorrow.json
│   ├── heavy-meetings-day.json
│   ├── blocked-task-present.json
│   ├── stale-index-fallback.json
│   └── calendar-overcapacity.json
└── reports/                    # Summaries produced by EvaluationAgent
```

---

## Decision Logs

- Format: JSON Lines (one JSON object per line)
- Location: `.agent-os/metrics/decision-logs/YYYY-MM/decision-log-YYYY-MM-DD.jsonl`
- Purpose: Enable post‑hoc evaluation, regression analysis, and weight tuning.

### Log Fields (minimum)

- `ts`: ISO timestamp
- `request_id`: unique id per recommendation request
- `user_context`: `{ time_available_min, energy, contexts[] }`
- `inputs`: `{ tasks_count, notes_count, retrieval_coverage, last_sync_age_s }`
- `candidate_count`: integer
- `chosen`: RecommendationResult (see product spec)
- `alternatives`: array of RecommendationResult (truncated)
- `constraints`: `{ renewal_protected, buffer_pct }`
- `evaluation`: `{ status, completed_in_block, outcome, elapsed_min, notes }`
- `errors`: array (if any)

### Example (JSONL)

```json
{
  "ts": "2025-10-03T19:45:21Z",
  "request_id": "req_8af2",
  "user_context": {
    "time_available_min": 30,
    "energy": "medium",
    "contexts": ["@Computer"]
  },
  "inputs": {
    "tasks_count": 124,
    "notes_count": 57,
    "retrieval_coverage": 0.78,
    "last_sync_age_s": 22
  },
  "candidate_count": 5,
  "chosen": {
    "action": "Review MKUH deployment status",
    "project": "FITFILE Platform",
    "duration_min": 45,
    "contexts": ["@Computer"],
    "energy": "medium",
    "score": 0.93,
    "confidence": 0.82,
    "why": "Big Rock aligned, due today, fits energy/time, unblocked."
  },
  "alternatives": [
    { "action": "Update central services config", "score": 0.88 }
  ],
  "constraints": { "renewal_protected": true, "buffer_pct": 25 },
  "evaluation": { "status": "planned" },
  "errors": []
}
```

---

## Golden Tests

Golden tests define canonical scenarios and assertions to protect critical behaviors (importance‑first logic, renewal protection, blocker avoidance, etc.).

- Source files live in `./golden/*.json`
- Each file contains `input` (context + tasks) and `expected` assertions
- EvaluationAgent loads each scenario, runs the pipeline, and checks assertions

### Common Assertions

- `must`: required conditions (e.g., top action contains text, matches project)
- `must_not`: forbidden conditions (e.g., recommending blocked tasks)
- `thresholds`: `score_min`, `confidence_min`
- `policy`: flags like `protect_renewal`, `respect_time_window`

---

## QA Workflow

1. Log every recommendation in JSONL (decision‑logs/)
2. Run golden tests on changes to scoring, retrieval, or prompts
3. EvaluationAgent produces a weekly report in `reports/`
4. Propose weight updates (e.g., confidence/freshness) and capture in PR

---

## Privacy & Retention

- Store only minimal necessary data
- Redact sensitive content before logging
- Rotate logs monthly; archive older than 90 days locally

---

## References

- `product/llm-framework-enhancements.md` for schemas and scoring
- `Productivity OS/01_Standards_Consolidated.md` for contexts/energy
