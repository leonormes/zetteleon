---
created: 2026-07-30T10:32:22+00:00
modified: 2026-07-30T10:32:22+00:00
permalink: llmeon/90-audits/2026-07-30-reality-testing
title: 2026-07-30-reality-testing
type: note
---

## Thread audit — [[Reality Testing]] — 2026-07-30

### Verdict

Reality Testing is not load-bearing — it is a thin, unscrutinised node that a couple of other notes gesture at rather than actually lean on. The two candidate relations that touch it are both recorded off-node, as free-text `rel::` lines inside the MOC rather than as anything on Reality Testing's own file, and neither survives testing as written: one is a direction/type error (an `instance_of` relation mislabelled `supports`), the other uses a relation word (`corrects`) that isn't in the controlled vocabulary at all and fails Substitution and Load outright. The weakest link is the seed itself — empty `type` and `tags`, no falsifier, no crux, and its only self-authored link goes to a daily journal entry, not an argument.

### Exposure list

| Note | Dependents | Falsifier? | Confidence dated | Exposure |
|---|---|---|---|---|
| [[Reality Testing]] (seed) | 0 confirmed after testing — the one candidate (Mind-Reading Fallacy and Projection, via the MOC's `corrects` line) fails Substitution and Load | No | No confidence/status field of any kind (`type: ''`, `tags: []`, `status: ''`) | Low, despite zero scrutiny — it doesn't hold anything up, so low dependents × low scrutiny nets out low, not high |
| [[Feedback-Seeking Strategies for Calibration]] | Not tested for its own downstream dependents this run | No | `status: seedling`, undated | Frontier — this note is the candidate *premise* for the seed, not its dependent; see Threads |
| [[Mind-Reading Fallacy and Projection]] | Not tested for its own downstream dependents this run | No | `conformant: false — "Bulk inferred type. Needs review."` | Frontier |

### Threads

#### Candidate 1 (downward/justification): [[Feedback-Seeking Strategies for Calibration]] → [[Reality Testing]]

- Evidence line (recorded in the MOC, not on either note): `[[Feedback-Seeking Strategies for Calibration]] rel:: supports [[Reality Testing]]`.
- Denial: passes, weakly — one could hold Feedback-Seeking Strategies' specific social-feedback techniques valid while denying they're what grounds Reality Testing's much broader claim (RT's own text: "the external world serves as a sounding board to test the validity of their thoughts and perceptions" — not scoped to social self-perception at all).
- Substitution: fails — swap Feedback-Seeking Strategies for any other external-validation mechanism (peer review, empirical testing, a second opinion) and Reality Testing's claim is served just as well. It reads as one instance of the phenomenon RT describes, not a uniquely necessary premise for it.
- Load: fails — if Feedback-Seeking Strategies' specific tactics (multi-rater checks, "how did that land for you") were shown ineffective, Reality Testing's general claim about external validation wouldn't move.
- Verdict: **RETYPE**, not sever — a real relation exists, but it's constitutive/taxonomic (Feedback-Seeking Strategies is a concrete instance of the general reality-testing mechanism), which the vocabulary marks `instance_of` — non-inferential. As `supports` it's a "constitution mistaken for support" pathology. Confidence: medium (relation is hub-recorded and structurally implied, not stated via an explicit inferential connective).

#### Candidate 2 (upward/implication): [[Reality Testing]] → [[Mind-Reading Fallacy and Projection]]

- Evidence line (recorded in the MOC, not on either note): `[[Reality Testing]] rel:: corrects [[Mind-Reading Fallacy and Projection]]`.
- Denial: passes — one can affirm both notes while denying reality-testing specifically is the corrective for mind-reading (CBT-style restructuring, direct disclosure, or time could just as well serve).
- Substitution: fails — swap in [[Feedback-Seeking Strategies for Calibration]], which supplies Mind-Reading Fallacy and Projection's own listed "corrective practices" verbatim ("Directly ask... rather than assuming"), and the argument is at least as strong. Reality Testing isn't the uniquely required note here.
- Load: fails — Mind-Reading Fallacy and Projection's account of the bias (inference-vs-fact confusion, projection, confirmation loop) is documented independent of any reality-testing construct; it doesn't move if Reality Testing is retracted.
- Verdict: **SEVER**. Also flag: `corrects` is not in the controlled vocabulary under either scheme in play — not AGENTS.md §9.3's six (`extends`, `synthesizes`, `implements`, `contradicts`, `supports`, `depends_on`), nor this audit's five (`supports`, `prerequisite_of`, `instance_of`, `contrasts_with`, `related_to`). It was never a legal edge regardless of the test outcome.

### Traversal manifest

| Node | Type | Depth | Direction | Termination |
|---|---|---|---|---|
| [[Reality Testing]] | zettelkasten atom, `type: ''` (unset) | 0 | seed | root — unargued; no falsifier, no typed edges of its own |
| [[Feedback-Seeking Strategies for Calibration]] | `type: strategy` | 1 | downward, hub-recorded `supports` | tip — RETYPE candidate (`instance_of`), not traversed further |
| [[Mind-Reading Fallacy and Projection]] | `type: concept` | 1 | upward, hub-recorded `corrects` | tip — SEVER, out-of-vocabulary relation |
| [[Meta-Accuracy in Social Perception]] | `type: concept` | 1 | inbound, bare `[[wikilink]]` in its own "### Related" list | NO EVIDENCE — no surrounding prose, no hub-recorded edge to the seed either |
| [[MOC - Social Perception and Self-Awareness]] | `type: map` | 1 | boundary | Domain Hub — record and stop; hosts both `rel::` lines above plus two purely procedural mentions of the seed ("Practical Entry Points", "When bias is suspected") |
| [[01_journals/Dailies/2025-05-26]] | daily/journal note, human territory (AGENTS.md §0) | 1 | outbound — the seed's only self-authored link | NO EVIDENCE — a bare wikilink alone on its own line, no surrounding prose; plausibly a capture-date convention, but that reading isn't supplied by anything written down, so it isn't asserted here |

No depth-cap truncation — every branch terminated at depth 1 (hub, no-evidence, or failed-test tip). Two `.trash/` files also match "Reality Testing" in full-text search (`2026-07-11-frontmatter-migration-dryrun.md`, `Heptabase/Card Library/CBT-Based Cognitive Restructuring Techniques Adapted for ADHD.md`) — excluded as deleted content, not part of the live graph.

### Patch A — proposed typings (high confidence only)

None. Both candidate edges are recorded only in the MOC (not as frontmatter or an inline edge on either endpoint note), and one is mistyped, the other out-of-vocabulary. Neither clears the high-confidence bar for promoting into a typed edge on Reality Testing itself.

### Patch B — sever candidates

| From | To | Reason | Evidence line |
|---|---|---|---|
| [[Reality Testing]] | [[Mind-Reading Fallacy and Projection]] | Fails Substitution and Load; relation word (`corrects`) isn't in the controlled vocabulary either | MOC: `[[Reality Testing]] rel:: corrects [[Mind-Reading Fallacy and Projection]]` |

[[Feedback-Seeking Strategies for Calibration]] → [[Reality Testing]] is deliberately not in this table — a real relation does exist, it's just mistyped (`instance_of`, not `supports`); see Candidate 1 above.

### No evidence — needs your call

| From | To | Where it sits |
|---|---|---|
| [[Mind-Reading Fallacy and Projection]] | [[Reality Testing]] | Bare item in Mind-Reading Fallacy and Projection's own "### Related" list — no prose sentence anywhere in that note names Reality Testing |
| [[Feedback-Seeking Strategies for Calibration]] | [[Reality Testing]] | Bare item in Feedback-Seeking Strategies' own "### Related" list — same gap; the only substantive claim about this pair lives in the MOC, not on either note |
| [[Meta-Accuracy in Social Perception]] | [[Reality Testing]] | Bare item in Meta-Accuracy's own "### Related" list — no prose, and no hub-recorded edge to the seed at all |
| [[Reality Testing]] | [[01_journals/Dailies/2025-05-26]] | The seed's only self-authored link — a lone wikilink with no surrounding sentence |

### Pathologies found

- **Constitution mistaken for support** — Feedback-Seeking Strategies `supports` Reality Testing should be `instance_of`; a concrete method is being typed as evidence for the general claim it instantiates.
- **Out-of-vocabulary relation** — `corrects` isn't in either controlled vocabulary in play. Worth knowing this isn't isolated: the MOC's own `rel::` lines elsewhere use `enables`, `distorts`, `relates-to`, `defines`, `is-calibrated-by`, `drives`, `underlies` — none of which are in AGENTS.md §9.3's six-word list either. Flagged here only as it touches the seed; the wider pattern is out of this run's scope.
- **Off-node edge recording** — both relations touching Reality Testing live in the MOC's prose, not as frontmatter or an inline `%%[…]%%` edge on either endpoint. `edge_lint.py` almost certainly can't see either one, meaning Reality Testing is likely already showing up as ungrounded (or simply absent) in the compiler's own graph, independent of anything found here.
- **Bare assertion, more severe than usual** — no falsifier, no crux, no dated confidence, and `type`/`tags` both empty. This isn't "under-grounded," it's "never entered the schema."
- **Not monoculture — no culture at all** — monoculture requires a single cited source; Reality Testing cites nothing. There isn't a source to be a monoculture of.

### Frontier

None beyond depth 1 — every branch terminated before a second hop (hub, no-evidence, or failed test). If Candidate 1 is retyped, [[Meta-Accuracy in Social Perception]] is the natural next hop (already `is-calibrated-by`-linked to Feedback-Seeking Strategies in the MOC).

### Next action

In `MOC - Social Perception and Self-Awareness.md`, delete or reword the line `[[Reality Testing]] rel:: corrects [[Mind-Reading Fallacy and Projection]]` — it's the one asserted edge here that fails Substitution and Load outright.
