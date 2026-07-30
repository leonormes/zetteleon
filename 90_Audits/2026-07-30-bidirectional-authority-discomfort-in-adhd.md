---
created: 2026-07-30T12:00:06+00:00
modified: 2026-07-30T12:00:06+00:00
permalink: llmeon/90-audits/2026-07-30-bidirectional-authority-discomfort-in-adhd
title: 2026-07-30-bidirectional-authority-discomfort-in-adhd
type: note
---

## Positioning — [[Bidirectional Authority Discomfort in ADHD]] — 2026-07-30

**Tooling tier: raw filesystem grep/read only** — no 1MCP `obsidian-mcp-tools`, no `obsidian` CLI this session. Coverage downgraded accordingly: lexical, not semantic.

### Baseline

A near-orphan, but not by accident — it's cited by exactly one file, its declared home hub. Frontmatter already carries the modern schema (`type: claim`, `conformant: false`, `non_conformance_reason: "Bulk inferred type. Needs review."`) plus a non-standard `source:` field pointing at `[[MOC - Authority Dynamics and ADHD]]`. No body wikilinks at all, no typed edges either direction.

- Inbound: [[MOC - Authority Dynamics and ADHD]] — real prose use, not a bare list entry: *"This [[Bidirectional Authority Discomfort in ADHD\|two-directional authority discomfort]] is common in people with ADHD."* Exactly one file in the whole vault references this note.
- Outbound: none in body. One reference exists only in the `source:` frontmatter field — functions as a link but isn't discoverable the way a normal backlink is, and isn't part of any documented frontmatter schema.
- Typed edges: none, either direction.

### Search Execution

- Literal anchor "Bidirectional Authority Discomfort" → confirms the single inbound reference above.
- Literal/conceptual variants `authority|power dynamic|hierarchy|being told what to do|directing others|rejection sensitiv` across `30_Library/` → 165 files, heavy noise (DNS delegation, container namespaces, org-chart SoTs sharing the word "authority" or "hierarchy" in an unrelated sense). Narrowed by hand to the ADHD/authority-psychology cluster below.

### Candidate Connections

| Candidate | Use/Mention evidence | Denial | Substitution | Load | Verdict |
|---|---|---|---|---|---|
| [[Rejection Sensitive Dysphoria (RSD)]] | Recorded only in the MOC's prose: *"This discomfort connects to Rejection Sensitive Dysphoria (RSD)... RSD can make authority interactions particularly challenging due to heightened sensitivity to judgment in both directions."* Neither note's own file mentions the other. | Passes — the Target already proposes its own competing explanation ("general sensitivity to power dynamics"), so RSD isn't the only account on offer; one could hold the phenomenon without RSD | Weakly fails to swap — RSD's specific "sensitivity to judgment" mechanism fits the *bidirectional* shape unusually well, not a generic stand-in | Partial — RSD losing validity wouldn't erase the phenomenon (Target has its own account) but would remove the MOC's stated amplifying mechanism | **Real but MEDIUM confidence** — direction and completeness genuinely uncertain (Target offers a rival/complementary explanation, not a restatement of RSD). Not writing it — see below |
| [[Implicit Social Hierarchies Authority]] | Keyword match only ("authority") — this note is about *deferring to others'* confident-sounding opinions (epistemic weighting), a different phenomenon from ADHD's *own* discomfort holding/being subject to authority | — | — | — | **NO EVIDENCE** — false positive from the grep, different concept sharing a word |
| [[SoT - Authority-Competence Asymmetry]] | Keyword match only ("authority", "hierarchy") — organisational dysfunction (positional vs. expert power), not personal psychological discomfort | — | — | — | **NO EVIDENCE** — same keyword-collision pattern |
| [[MOC - ADHD (The Master Map)]] | Doesn't mention the Target or [[MOC - Authority Dynamics and ADHD]] at all | — | — | — | Structural aside, not this note's problem: the home hub itself isn't linked from the top-level ADHD map. Flagging, not fixing — out of scope for a single-note run |

### Patch A — Typed Edge to Write (six-word vocabulary only)

None this run. The one real candidate (RSD) is medium confidence — the protocol is explicit that medium-confidence typings don't get written, they get reported. See "No evidence / needs your call" below.

Worth noting as a positive precedent while we're in this cluster: [[Rejection Sensitive Dysphoria (RSD)]] already carries two correctly-formed edges on its own file — `%%[supports:: [[Collaborative Programming Mitigates RSD and Focus Issues in ADHD]]]%%` and `%%[supports:: [[ADHD Emotional Reasoning]]]%%` — so the closed vocabulary is already live and working elsewhere in this exact neighbourhood.

### Patch B — Plain Links / MoC Anchors (you'd apply these)

| File | Proposed line | Where it goes |
|---|---|---|
| [[Bidirectional Authority Discomfort in ADHD]] | *"This pattern is explored further in [[MOC - Authority Dynamics and ADHD]], which also connects it to [[Rejection Sensitive Dysphoria (RSD)\|Rejection Sensitive Dysphoria]]."* | New line in the Target's own body — promotes the hub connection out of the non-standard `source:` field into a real, annotated body link, and surfaces the RSD connection as prose (honest about it being a proposed mechanism, not a tested edge) |

### Patch C — Frontmatter Conformance (you'd apply this)

| Field | Current | Proposed |
|---|---|---|
| `non_conformance_reason` | `"Bulk inferred type. Needs review."` | Replace once the fields below are filled — the generic bulk-migration reason can be cleared |
| `proposition` (ClaimNote §3.1, missing) | — | `"People with ADHD often experience authority discomfort bidirectionally—resisting external direction and discomfort directing others—reflecting a general sensitivity to power dynamics rather than a desire for personal power."` |
| `epistemic_status` (missing) | — | `medium` — the MOC itself frames this as "based on personal reflections," not on cited research |
| `evidence_links` (missing) | — | none available — no `type: evidence` note exists yet for this claim; leaving empty rather than inventing one |

### Claim Stubs Written

None. The Target's own alternative framing ("general sensitivity to power dynamics") reads as part of this claim, not a distinct concept needing its own note.

### No evidence / needs your call

| Candidate | Why it stayed a proposal, not a write |
|---|---|
| [[Rejection Sensitive Dysphoria (RSD)]] | Real connection, medium confidence only — direction is genuinely ambiguous (does RSD `support` this claim, or does this claim `depend_on` RSD as one of several contributing mechanisms?). Your call on which, if either. |
| The `source:` frontmatter field | Functions as a link today but isn't part of any documented schema — Patch B turns it into a normal body link; whether to also remove the frontmatter field is your call, not proposed here |

### Validation

- `edge_lint.py`: not run — nothing was written this run.
- Confidence: high on the "no edge" verdicts for the two false-positive candidates; medium (explicitly not written) on RSD.

---

## Next action

Tell me whether to apply Patch B (the plain link) and/or Patch C (frontmatter fields) — there's no Patch A this run, so there's nothing to lint yet.
