---
created: 2026-09-25T00:00:00+00:00
modified: 2026-09-25T00:00:00+00:00
permalink: llmeon/90-audits/2026-09-25-paxos-vs-raft-correctness-vs-intuition
title: 2026-09-25-paxos-vs-raft-correctness-vs-intuition
type: note
---

## Positioning — [[Paxos vs Raft (Correctness vs Intuition)]] — 2026-09-25

> Second run of [[Orphan Note Positioning & Thread Audit]], following [[2026-09-25-byzantine-fault-tolerance-requirements]]. It is one of the seven same-source atoms listed in `_link_report_concurrency_challenges`.

### Baseline

- Thin. Outbound: 3 plain links (SoT - Pragmatism vs Rigour in Software, The Illusion of Fluency..., SoT - State Synchronization Models) plus `upstream` to SoT - Rust Concurrency & Async Paradigms. Inbound: only the link report and, since the previous run, the BFT note.
- No typed edges. Frontmatter non-conformant: `type: atom`, no `conformant`, `proposition` or `epistemic_status`.
- Not a node in the argument graph (`--why` and `--impact` both: no node found).
- Tooling: Obsidian MCP (`wikilinks`) plus `rg` for exact-literal hunts. `search_semantic` was not retried after erroring last run, so coverage is lexical and confidence in "nothing missed" is medium.

### Search Execution

- `Paxos`, `Raft`, `etcd`, `consensus` (literal anchors, `rg` across `30_Library`): the Target, BFT note, etcd atoms, Kubernetes MoCs, `SoT - Conservation of Complexity`.
- Read to confirm content: `etcd stores cluster network state and service configuration` (states Raft), `Loss of etcd or the API Server...` (names quorum loss; no Raft or Paxos mention), `Invariants vs Behavioural Sequences`, `SoT - Pragmatism vs Rigour in Software` (section 7 layout), `MOC - The Trade-off Between Pragmatism and Rigour...` (inclusion criteria).
- Hub scan: `MOC - Computer Science Foundations` (already carries the BFT line), the Pragmatism-versus-Rigour MoC.

### Candidate Connections

| Candidate | Use/Mention evidence | Denial | Substitution | Load | Verdict |
|---|---|---|---|---|---|
| [[SoT - Pragmatism vs Rigour in Software]] | Target: "prioritises intuitive understandability... over formal mathematical rigour"; SoT defines exactly that conflict | Claim survives as an observation | Other notes name the conflict less directly | Structural only | `implements` |
| [[The Illusion of Fluency is a Cognitive Bias Where Ease of Processing is Mistaken for Deep Learning]] | Target's Implications lean on ease of understanding standing in for verification | Interpretation weakens, observation survives | The bias is specific to this note | Structural only | `implements` |
| [[Byzantine Fault Tolerance Requirements]] | Same video, failure-model question precedes protocol choice | Topical | Yes | No | plain link |
| [[Invariants vs Behavioural Sequences]] | Says invariant-based proof is the scalable route to correctness, the rigour side of this trade-off | Claim survives | [[SoT - Mathematical Proof Techniques]] would serve partly | Weak | plain link (a `supports` edge would create a new gap for weak return) |
| [[etcd stores cluster network state and service configuration]] | States "Raft algorithm for data consistency" | Topical instance | Yes | No | plain link |
| [[Loss of etcd or the API Server Disables the Whole Kubernetes Control System]] | Names quorum loss as the failure; does not mention Raft | Topical | Yes | No | plain link, annotation limited to quorum |
| [[SoT - Abstracting Concurrent Systems]] | TLA+ and invariants as the formal-specification route | Topical | Yes | No | plain link |

### Patch A — Typed Edges

| Target file | Edge line | Rationale | Resolved? |
|---|---|---|---|
| Paxos vs Raft (Correctness vs Intuition) | `[implements:: [[SoT - Pragmatism vs Rigour in Software]], confidence=medium]` | Instance of the SoT's central conflict | Yes |
| Paxos vs Raft (Correctness vs Intuition) | `[implements:: [[The Illusion of Fluency is a Cognitive Bias Where Ease of Processing is Mistaken for Deep Learning]], confidence=medium]` | Case of the bias | Yes |

Both are structural, so the compiler ignores them for gap and exposure counts. I chose that over `supports`/`depends_on` because neither target grounds the observation, and the vault already has 40 open gaps.

### Patch B — Plain Links / MoC Anchors

| File | Proposed line | Where it goes |
|---|---|---|
| Target | Five annotated links | New `### Cluster and Neighbours` section |
| SoT - Pragmatism vs Rigour in Software | `- Case study, consensus protocols: [[Paxos vs Raft (Correctness vs Intuition)]]` | End of section 7, Related Components (primary home) |
| MOC - Computer Science Foundations | Entry "The Consensus Trade-off" | Directly after the BFT entry in section 4 (secondary home) |

The Pragmatism-versus-Rigour MoC was rejected as a hub: its stated inclusion criteria admit only canonical SoT notes, and this is an atom.

### Patch C — Frontmatter Conformance

| Field | Current | Proposed (applied) |
|---|---|---|
| `type` | `atom` | `claim` |
| `conformant` / `non_conformance_reason` | absent | `true` / `''` |
| `proposition` | absent | one sentence, no colons or quotes |
| `epistemic_status`, `evidence_links`, `contradicts` | absent | `medium`, `[]`, `[]` |

### Patch D — Further Reading, Personal Library

None. Two ARCHILLES queries returned the nearest hits below the 0.30 relevance floor: *Database Internals* p. 300 (0.237, Paxos generalisation, no comment on understandability), *Site Reliability Engineering* p. 385 (0.216, Paxos variations). *Understanding Distributed Systems* (0.209) cites the papers "In Search of an Understandable Consensus Algorithm" and "Paxos Made Simple" in a footnote. That gives titles to check, not evidence.

### Applied (Part 2)

| File | Change | Status |
|---|---|---|
| Paxos vs Raft (Correctness vs Intuition) | Frontmatter conformance; appended `### Typed Relationships`, `### Cluster and Neighbours`, `### Tensions` (existing prose untouched) | Done |
| SoT - Pragmatism vs Rigour in Software | One line under Related Components | Done |
| MOC - Computer Science Foundations | One line in section 4 | Done |

### Claim Stubs Written

None.

### No evidence / needs your call

| Candidate | Why untestable |
|---|---|
| Whether Raft is less reliable in practice than Paxos | The Target only asserts a selection bias, from one quoted sentence. Flagged in its `### Tensions`. Checking the Raft paper and "Paxos Made Simple" would settle whether the source says more. |
| A dedicated note on Raft (or crash-fault consensus) | None exists. Not created: nothing in the Target needs it as an edge target. |
| Whether `SoT - Conservation of Complexity` belongs here | It matched the `Raft`/`consensus` grep but I did not read it, so I made no claim about it. |

---

## Thread Audit (Part 3)

### Verdict

The Target is not a node in the argument graph. `--why` and `--impact` both report no node found, because it carries only `implements` edges. Exposure 0, no dependents, no threads, as expected. No thread is invented.

### Traversal manifest

- Outbound: 2 typed `implements` edges, 5 new plain links, 3 pre-existing plain links plus `upstream`. Inbound: BFT note, link report, this audit.
- Use-vs-mention on the pre-existing plain links: the Pragmatism SoT and the Fluency note are now typed. `SoT - State Synchronization Models` stays a plain See Also, which is accurate (it lists Merkle and reconciliation models, not consensus).

### Pathologies

- The `[[...)]]`-style broken bracket in the Happens-before atom's `upstream` (`[[SoT - Rust Concurrency & Async Paradigms)]]`) is a sibling problem, not this note's. Lint does not flag it. Worth fixing when that atom's turn comes.
- Gap count unchanged at 40, since only structural edges were added.

### Validation

- `edge_lint.py` (whole vault): 0 errors, 0 warnings (2908 notes, 1413 edges).
- Confidence: medium. Lexical search only, and the reliability question rests on one quoted sentence.

## Next action

Run `Orphan Note Positioning & Thread Audit` on [[Happens-before as Logical Ordering]], which has the malformed `upstream` link and the weakest existing connections of the five remaining siblings.
