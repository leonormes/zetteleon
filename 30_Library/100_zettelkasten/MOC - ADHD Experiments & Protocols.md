---
aliases: ["ADHD Lab", "ADHD Strategy Experiments", "Protocol Testing"]
confidence: "5/5"
created: 2025-12-16T12:00:00Z
epistemic: "experimental"
last_reviewed: "2025-12-16T00:00:00.000Z"
modified: 2025-12-28T09:56:31+00:00
purpose: ""
review_interval: "null"
see_also: []
source_of_truth: []
status: "active"
tags: ["experiments", "hypothesis", "moc", "protocols", "topic/health/adhd", "topic/productivity"]
title: MOC - ADHD Experiments & Protocols
type: "map"
uid: 
updated: 
---

> [!dashboard] Live View
> For the full status board of all experiments, see: **[[Lab Experiments.base]]**

## 1. The Laboratory Mandate

> [!abstract] Reality as a Unit Test
> A note in the vault is useless until it is tested in reality. We do not collect "good ideas"; we curate **validated protocols**.
>
> This MOC tracks the lifecycle of an ADHD strategy:
> `Hypothesis (Note) -> Experiment (Action) -> Validation (SoT) or Rejection (Archive)`

---

## 2. The Experiment Protocol

To move a strategy from "Candidate" to "Validated," follow this 3-step loop:

1. **Define:** Convert a note into a `type: hypothesis`. Define the **Context** and **Expected Outcome**.
2. **Test:** Mark status as `active`. Commit to the protocol for 1 week. Log results in the note.
3. **Review:** Rate the efficacy.
    - *Pass:* Mark `status: validated`. Merge findings into the relevant [[SoT - ADHD Executive Dysfunction]].
    - *Fail:* Mark `status: rejected`.

---

## 3. Active Experiments (The Workbench)

```dataview
TABLE without id file.link as "Experiment", purpose as "Hypothesis"
FROM #hypothesis
WHERE status = "active"
```

---

## 4. Candidate Protocols (The Backlog)

*Potentials awaiting definition.*

```dataview
TABLE without id file.link as "Candidate", purpose as "Goal"
FROM #hypothesis
WHERE status = "pending"
```

---

## 5. Validated Protocols (The System)

*Strategies that have passed the test.*

```dataview
TABLE without id file.link as "Protocol", source_of_truth as "SoT Link"
FROM #hypothesis
WHERE status = "validated"
```

---

## 6. Rejected Protocols (The Graveyard)

```dataview
TABLE without id file.link as "Failed Experiment"
FROM #hypothesis
WHERE status = "rejected"
```
