---
created: 2026-09-24T00:00:00+00:00
modified: 2026-09-24T00:00:00+00:00
permalink: llmeon/90-audits/2026-09-24-cybernetics
title: 2026-09-24-cybernetics
type: note
---

## Positioning — [[Cybernetics]] — 2026-09-24

> Second pass; the first was [[2026-07-31-cybernetics]], which added the `extends` edge. Lexical search only (1MCP tools were unavailable).

### Prompt routing

Per [[00 - Prompt Library Router]]: **zero inbound links** from any vault note and one outbound typed edge, so it is a genuine orphan in the "few or no links" sense. Routed to [[Orphan Note Positioning & Thread Audit]] (v3, one run).

### Baseline

- **Inbound:** none. **Outbound:** three Related links and `[extends:: [[SoT - Systems Thinking]]]`. **Broken links:** none (resolver: 0 unresolved).
- **Frontmatter:** already conformant, but `epistemic_status: high` with no evidence.
- **Cluster:** at least ten notes in the vault apply feedback loops in one domain (ecology, cognition, agents, ADHD motivation, Kubernetes) and none pointed at the note that defines the idea.

### Candidate connections

| Candidate | Verdict |
|---|---|
| The ten-note feedback-loop family (Overshoot and Collapse, Kaibab, Cultural Ritual, Prediction Error, Agent Feedback Loops, Rapid Feedback ADHD, Competence Feedback Loop, Action-Reaction-Ping-Adjust, Kubernetes analysis, Korzybski) | Use: each applies the core idea. None passes the denial test as a logical dependency on this definition, so **plain links**, not edges |
| [[SoT - Systems Thinking]] | Already `extends`; now also links back |
| ProdOS loops: [[SoT - PRODOS - The Cognitive Loop (A-C-T Framework)]], [[SoT - ProdOS Thinking Stream]], [[Protocol - Weekly Command Centre]], [[Protocol - Autonomous Action System]], [[Protocol - Diagnose an Agent Failure]] | Use, with annotations naming which part is the loop. Plain links |

### Changes

| File | Change |
|---|---|
| The note | `evidence_links` → the new Evidence note; `### The Feedback-Loop Family` (10 links), `### Where It Applies in ProdOS` (5), `### Further Reading` (2 books). Definition and existing edge untouched |
| **New:** [[Evidence - Gleick on Wiener Frames Cybernetics as Negative Feedback Control Where Information Is the Key]] | Verbatim quote from *The Information* (Calibre 101). Confidence 0.6 |
| SoT - Systems Thinking | bullet in its links section, giving Cybernetics its first inbound link |

**No new typed edges.** `epistemic_status: high` is kept, since it is a standard definition and now has an evidence note; the Evidence note says what it does not show.

### Library evidence

- **Kept:** *The Information* (Gleick, on Wiener: negative feedback, the steam-engine governor, "the key to the process is information") and *What Is Life?* (Nurse: negative and positive feedback modules in cells). Both passages read in full.
- **Discarded:** the software-engineering and mathematics hits (Scala with Cats, Code Complete, Release It!, Data Mesh and similar) matched on "feedback" or "control" only.

### Thread audit

`--why`: supported by the Evidence note. `--impact`: nothing rests on it, so exposure is 0 and there is no gap. It is now reachable from the parent SoT.

### Left alone

- [[Emergence]] (linked from this note's Related) is a template stub with "Suggested Links" placeholders.
- [[Cybernetic Analysis of Kubernetes State Management.]] has `type: null`, a trailing period in its title, and sits in the zettelkasten folder although its permalink says `200-projects`; I linked it as it is.
- The permalink `7-cybernetics-1` shows the note descends from an old Luhmann-style `7-cybernetics`; the "-1" suffix suggests a duplicate that was renamed. I did not look for one.

### Validation

Whole-vault `edge_lint.py`: `0 error(s), 0 warning(s)` (2866 notes, 1389 edges). Confidence: **medium**.
