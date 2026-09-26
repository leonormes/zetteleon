---
created: 2026-09-25T00:00:00+00:00
modified: 2026-09-25T00:00:00+00:00
permalink: llmeon/90-audits/2026-09-25-byzantine-fault-tolerance-requirements
title: 2026-09-25-byzantine-fault-tolerance-requirements
type: note
---

## Positioning — [[Byzantine Fault Tolerance Requirements]] — 2026-09-25

> Routed to [[Orphan Note Positioning & Thread Audit]] per [[00 - Prompt Library Router]]: one thin note whose cluster was never wired into the wider graph. The cluster is the seven atoms from one video, listed in `_link_report_concurrency_challenges`. [[LLM Graph Bootstrap Agent]] is the right follow-up for the cluster as a whole (see Next action).

### Baseline

- Thin, not a true orphan. Outbound: 3 plain links (Encryption vs Digital Signatures, SoT - Network Security Architecture, SoT - Microsoft Entra Identity) plus `upstream` to SoT - Zero Trust Architecture. Inbound: 6 atoms and one index note, all boilerplate Entra and Zero Trust notes whose links use generic wording such as See Also.
- No typed edges. Frontmatter was non-conformant: `type: atom`, no `conformant`, `proposition` or `epistemic_status`.
- Not a node in the argument graph before this run (`--why` reported no node found).
- Tooling: Obsidian MCP (`search_text`, `wikilinks`). `search_semantic` errored twice, so coverage is lexical, not semantic. Confidence in "nothing missed" is therefore medium.

### Search Execution

- `Byzantine` (literal anchor): the Target, SoT - Abstracting Concurrent Systems (section 3.1), 6 inbound notes, the link report.
- `consensus quorum replication fault tolerance` (conceptual, title/heading/tag fields): Paxos vs Raft plus unrelated scientific-consensus notes.
- `Two Generals problem FLP impossibility Paxos Raft` (functional): Paxos vs Raft only. No FLP, CAP or Two Generals notes exist.
- `digital signature authenticity non-repudiation forgery` (functional): Encryption vs Digital Signatures, SoT - Cryptography and Encryption, SoT - Modern Authentication Standards.
- `distributed systems` (literal): SoT - Abstracting Concurrent Systems, A Single System Image..., Git content-addressed object store, State Synchronization Models.
- Directory listing of `MoC/`, `SoT/` and `100_zettelkasten/` for hubs and same-source siblings.

### Candidate Connections

| Candidate | Use/Mention evidence | Denial | Substitution | Load | Verdict |
|---|---|---|---|---|---|
| [[SoT - Abstracting Concurrent Systems]] | Section 3.1: "Require a Threshold (Quorum) of signatures (n > 3f)"; applies the Target's arithmetic to authorisation | Deny it and section 3.1's threshold has no stated grounds | No other note carries the number | Retracting the Target lowers confidence in section 3.1 | `supports` (Target to SoT) |
| [[Encryption vs Digital Signatures - Confidentiality vs Authenticity]] | Target: "signatures provide the authenticity required to reduce node count" | Deny unforgeable authenticity and the 2n + 1 reduction is incoherent | Only signatures do this job | Retracting it moves the 2n + 1 half of the Target | `depends_on` |
| [[Paxos vs Raft (Correctness vs Intuition)]] | Same video, consensus protocols; the Paxos note says nothing about failure models | Topical only | Any consensus note would do | No | plain link |
| [[Invariants vs Behavioural Sequences]], [[Happens-before as Logical Ordering]], [[Mutual Exclusion without Hardware Atomicity]] | Same-video siblings | Topical | Interchangeable | No | plain links |
| [[Git's Content-Addressed Object Store Absorbs Distributed-Trust Complexity Into Structure]] | Tamper-evidence via structure, an alternative mechanism | Topical | Yes | No | plain link |
| [[SoT - State Synchronization Models]], [[SoT - Cryptography and Encryption]], [[SoT - Zero Trust Architecture]] | Blockchain exemplar; signature mechanism; assume-compromise parallel | Topical | Yes | No | plain links |
| 6 inbound Entra and Zero Trust atoms | Their "shared mechanism" annotations for the Target are generic | n/a | n/a | n/a | not touched (see needs your call) |

### Patch A — Typed Edges

| Target file | Edge line | Rationale | Resolved? |
|---|---|---|---|
| Byzantine Fault Tolerance Requirements | `[supports:: [[SoT - Abstracting Concurrent Systems]], confidence=medium]` | Evidence behind the n > 3f threshold | Yes |
| Byzantine Fault Tolerance Requirements | `[depends_on:: [[Encryption vs Digital Signatures - Confidentiality vs Authenticity]], confidence=high]` | 2n + 1 rests on unforgeable signatures | Yes |

No `contradicts` edge: the 3n + 1 versus 2n + 1 discrepancy passes the both-can-hold test, so it is a Tension.

### Patch B — Plain Links / MoC Anchors

| File | Proposed line | Where it goes |
|---|---|---|
| Target | Eight annotated links (cluster siblings, Git, three SoTs) | New `### Cluster and Neighbours` section |
| SoT - Abstracting Concurrent Systems | `- Evidence for section 3.1: [[Byzantine Fault Tolerance Requirements]]` | End of `## Related Knowledge` (primary home) |
| MOC - Computer Science Foundations | One annotated entry, "The Fault Model" | End of section 4, Cloud & Infrastructure (secondary home; no distributed-systems section exists) |

### Patch C — Frontmatter Conformance

| Field | Current | Proposed (applied) |
|---|---|---|
| `type` | `atom` (non-canonical) | `claim` |
| `conformant` / `non_conformance_reason` | absent | `true` / `''` |
| `proposition` | absent | one sentence stating the 3n + 1 and 2n + 1 claim |
| `epistemic_status`, `evidence_links`, `contradicts` | absent | `medium`, `[]`, `[]` |
| `kind`, `status`, `upstream`, `source_*` | present | unchanged |

### Patch D — Further Reading, Personal Library

None. Three ARCHILLES semantic queries (Byzantine generals; signed messages and any number of faults; state-machine replication with malicious replicas) returned nothing above the relevance floor whose text bears on the claim. The nearest hits were *Database Internals* on gossip and failure detection and *Understanding Distributed Systems* on reliable broadcast, neither about Byzantine faults. Recorded as a normal zero-match outcome.

### Applied (Part 2)

| File | Change | Status |
|---|---|---|
| Byzantine Fault Tolerance Requirements | Frontmatter conformance; appended `### Typed Relationships`, `### Cluster and Neighbours`, `### Tensions` (existing prose untouched) | Done |
| SoT - Abstracting Concurrent Systems | One line added under Related Knowledge | Done |
| MOC - Computer Science Foundations | One line added in section 4 | Done |

### Claim Stubs Written

None.

### No evidence / needs your call

| Candidate | Why untestable |
|---|---|
| 2n + 1 versus n > 3f with signatures | The vault's two statements differ and neither names its assumptions (synchronous or partially synchronous, signed or oral messages). Flagged as UNSURE in the Target's `### Tensions`; needs a primary source. |
| FLP, CAP, Two Generals, PBFT notes | Confirmed absent by title and text search. Not created because nothing in the Target needs them as a `supports` or `depends_on` target. |
| Six inbound Entra and Zero Trust atoms (Centralisation Risk, Global Administrator Limit, etc.) | Each links the Target with a generic "shared mechanism" annotation that I judge weak (redundancy against lying nodes versus break-glass accounts). Not my Target, so left alone; you may want them demoted. |

---

## Thread Audit (Part 3)

### Verdict

The Target is now a node with one premise and one dependent. Exposure is low but non-zero.

- `--why`: rests on [[Encryption vs Digital Signatures - Confidentiality vs Authenticity]] (premise). Bottoms out there.
- `--impact`: [[SoT - Abstracting Concurrent Systems]] (supports).
- `--audit`: gaps went from 38 to 40. Both new gaps are the two nodes I made load-bearing (the Target is now a `supports` source with no grounds, and Encryption vs Digital Signatures is now depended on with no grounds).

### Thread

- Root: Encryption vs Digital Signatures (no grounds). Chain: Target. Tip: SoT section 3.1.
- Weakest link: the Target's own evidence is a single sourced quote from a talk, with no Evidence note. The 2n + 1 figure is contestable (see Tensions).
- Cheapest defeater: a primary-source passage showing signed-message bounds depend on synchrony. If it holds, the `depends_on` edge stays but the claim needs scope conditions added.

### Traversal manifest

Outbound: 2 typed edges, 8 plain links, 3 pre-existing plain links. Inbound: 7 (6 atoms, 1 index). Use-vs-mention on the inbound links: all six atoms mention rather than use the Target, and none carries an inferential edge.

### Pathologies

- Two new C1 gaps (above), left open deliberately. Setting `axiom: true` on either would misdescribe them: the Target is sourced empirical content, not a chosen premise, and Encryption vs Signatures is a well-established result awaiting an Evidence note.
- The Target's `upstream` points at Zero Trust, which is a weak topical fit for a distributed-consensus claim. Left as is.

### Validation

- `edge_lint.py` (whole vault): 0 errors, 0 warnings (2907 notes, 1411 edges).
- Confidence: medium. Search was lexical (semantic search errored), and the 2n + 1 point rests on my recollection, not on a checked source.

## Next action

Run `Orphan Note Positioning & Thread Audit` on [[Paxos vs Raft (Correctness vs Intuition)]], the most graph-relevant of the six sibling atoms still unwired from the same video.
