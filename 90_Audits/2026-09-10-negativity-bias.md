---
title: 2026-09-10-negativity-bias
type: note
permalink: llmeon/90-audits/2026-09-10-negativity-bias
---

## Positioning — [[Negativity Bias]] — 2026-09-10

### Baseline

Frontmatter: `conformant: false`, `non_conformance_reason: "Bulk inferred type. Needs review."`, `type: concept` (already a valid FrontmatterContract value—just never confirmed conformant). Missing the ConceptNote-specific fields (`definition`, `distinguishes_from`, `used_in_claims`) from §3.2.

Existing link count in: **2** (via full-vault `grep`—MCP backlink tool unavailable this session, lexical-only confidence): [[SoT - The Negativity Bias]] §6 already names this note "The core concept," and [[MOC - Why Thoughts Feel More Important When Thinking Them]] references it.
Existing link count out: **0**.

Verdict: **not a true orphan—thin.** It already has a real parent (the SoT explicitly claims it), but zero outbound structure and no reciprocal link back. This still fits this prompt's trigger ("few or no links... not just under-linked" — the note has real inbound anchoring already established but is entirely undeveloped outbound, which is exactly the positioning gap this prompt exists to close).

### Search Execution

Concepts extracted: (1) negativity bias itself / "bad is stronger than good," (2) evolutionary threat-detection asymmetry, (3) loss aversion / asymmetric valuation, (4) cognitive bias taxonomy generally, (5) criticism/feedback reception (a specific application domain).

- `\[\[Negativity Bias\]\]` / `Negativity Effect` (literal anchor) → 2 inbound hits (above).
- `loss aversion` (conceptual variant) → [[Loss Aversion Describes Asymmetric Pain of Loss vs Pleasure of Gain]], [[Prospect Theory Models Decision-Making Relative to a Reference Point]] — both already cross-linked to each other and named by the parent SoT as "the economic parallel."
- `cognitive bias` MOC search (functional equivalent—where would this bias be catalogued?) → [[MOC - Cognitive Biases]], a live taxonomy hub with sections for Knowledge/Learning, Social/Self-Perception, and Decision-Making biases—Negativity Bias fits none of the three cleanly (it's closer to a fourth, unlisted category: threat/emotional-weighting biases) and isn't currently listed at all.
- `criticism|feedback` (functional equivalent—the practical domain where this bias bites) → [[Cognitive Reframing of Criticism]] (a `procedure`-type countermeasure), [[Feedback-Seeking Strategies for Calibration]], [[Distorted Negative Self-Image]] (a **different context entirely**—Bessie/parenting, ADHD self-assessment).
- `doomscroll|news consumption|media negativity|Gottman|positivity ratio` → no hits. The vault has no media-consumption or relationship-ratio angle on this bias yet—a real coverage gap, not a search failure.
- While reading the parent SoT, found two of **its own** broken links: `[[Humans Are Social Creatures]]` and `[[Why External Validation is So Powerful]]`—both dangling, no matching note or alias anywhere. Out of scope for this run (they're on the SoT, not the Target) but flagged under Pathologies.

### Candidate Connections

| Candidate | Use/Mention evidence | Denial | Substitution | Load | Verdict |
|---|---|---|---|---|---|
| [[SoT - The Negativity Bias]] | The SoT's entire argument (§3 "ADHD Amplifier," §5 countermeasures) is built directly on top of the Target's claim being true—it isn't just adjacent, it's load-bearing. | **Yes**—deny the Target's claim and the SoT's §3–§5 collapse; there's nothing left to amplify or counter. | No substitute—this is the specific note the SoT's own text names as its core concept. | **Yes**—if the Target's claim were false, confidence in the SoT's entire applied framework would move with it. | **Passes all three — Patch A.** |
| [[MOC - Cognitive Biases]] | Taxonomy membership only; the MOC doesn't reference this bias's specific content. | No—the MOC's own content is unaffected either way. | High—it's a container, substitutable by definition. | No. | **Topical — Patch B (MoC anchor).** |
| [[Loss Aversion Describes Asymmetric Pain of Loss vs Pleasure of Gain]] | Same "bad outweighs good" asymmetry, applied to decision-making; the parent SoT calls it "the economic parallel," but Loss Aversion's own body cites Kahneman/Tversky independently, not this bias. | No—Loss Aversion's specific empirical claim (the ~2x ratio) stands on its own evidentiary basis. | Weak—no better single match exists, but that alone doesn't establish dependency. | No—retracting the Target wouldn't undermine Loss Aversion's own cited evidence. | **Topical — Patch B.** |
| [[Prospect Theory Models Decision-Making Relative to a Reference Point]] | Same relationship as Loss Aversion (one level removed—reaches this note only via Loss Aversion). | No. | High. | No. | **Topical — Patch B.** |
| [[Cognitive Reframing of Criticism]] | A practical countermeasure to disproportionate reaction to criticism—thematically the exact behaviour this bias predicts, but its own text motivates itself independently (defensive hyperarousal, Stoic dichotomy of control) without naming this bias. | No—the procedure is self-justifying without invoking negativity bias by name. | Moderate. | No. | **Topical — Patch B.** |
| [[Distorted Negative Self-Image]] | **Different context** (family/Bessie, ADHD self-assessment): "without consistent, clear feedback... interpret her performance... distorted negative self-image." A concrete instance of the same asymmetric-weighting mechanism in a parenting/assessment setting rather than ADHD-adult or economics. | No—stands as its own claim about ambiguous-feedback interpretation. | Moderate. | No. | **Topical — Patch B, but valuable: this is the "different context" the brief asked for.** |
| [[Cognitive Biases Reinforce Mental Models]] | General epistemics claim (confirmation bias, cognitive dissonance, Dunning-Kruger reinforcing existing models)—adjacent bias-family member, not the same mechanism. | Yes. | High. | N/A. | **Rejected—same broad family, no specific shared claim.** |
| [[SoT - The Evolutionary Biology of Status]] | Shares "evolutionary threat-response" framing but is specifically about status/hierarchy, not valence-weighting of information. | Yes. | High. | N/A. | **Rejected—word-adjacent ("evolutionary"), not conceptually shared.** |

### Patch A — Typed Edges to Write (six-word vocabulary only)

| Target file | Edge line | Rationale | Resolved? |
|---|---|---|---|
| [[SoT - The Negativity Bias]] | `[depends_on:: [[Negativity Bias]], strength=5, confidence=high]` | The SoT's ADHD-amplifier and countermeasure sections presuppose the atomic claim; passes Denial and Load cleanly (see table). Edge lives on the SoT's file, not the Target's, per this prompt's "target file if direction runs the other way" rule—the SoT is the dependent party. | Yes—both notes confirmed to exist and resolve. |

### Patch B — Plain Links / MoC Anchors (Leon applies)

| File | Proposed line | Where it goes |
|---|---|---|
| [[Negativity Bias]] | `- [[SoT - The Negativity Bias]]—*the full applied framework this atom underpins (ADHD amplification via RSD, DMN rumination, and the countermeasures)—already cites this note as its core concept; this is the reciprocal link.*` | New `## Related` section |
| [[Negativity Bias]] | `- [[Loss Aversion Describes Asymmetric Pain of Loss vs Pleasure of Gain]]—*the decision-economics manifestation of the same "bad outweighs good" asymmetry—independently evidenced (Kahneman/Tversky), not a dependency.*` | Same section |
| [[Negativity Bias]] | `- [[Cognitive Reframing of Criticism]]—*a practical countermeasure for the exact behaviour this bias predicts: disproportionate emotional weight given to negative feedback.*` | Same section |
| [[Negativity Bias]] | `- [[Distorted Negative Self-Image]]—*a different context entirely: the same asymmetric-weighting mechanism applied to a child's self-assessment under ambiguous feedback, not adult ADHD or economics.*` | Same section |
| [[MOC - Cognitive Biases]] | `- [[Negativity Bias]]: The tendency to weight negative information and experiences more heavily than positive ones of equal intensity—an evolutionary threat-detection leftover.` | New subsection, e.g. "Threat & Emotional-Weighting Biases" (the MOC currently has no category for this; its three sections are Knowledge/Learning, Social/Self-Perception, Decision-Making) |

### Patch C — Frontmatter Conformance (Leon applies)

| Field | Current | Proposed |
|---|---|---|
| `conformant` | `false` | `true` |
| `non_conformance_reason` | `"Bulk inferred type. Needs review."` | (remove—no longer applicable) |
| `definition` | (missing) | `"The tendency for negative events, information, and experiences to have a greater psychological impact and receive more attention than neutral or positive ones of equal intensity—an evolutionary leftover from when threat-alertness was more survival-critical than opportunity-recognition."` |
| `distinguishes_from` | (missing) | `["[[Loss Aversion Describes Asymmetric Pain of Loss vs Pleasure of Gain]]"]`—*a specific decision-theoretic manifestation, not this concept's full scope* |
| `used_in_claims` | (missing) | `["[[SoT - The Negativity Bias]]"]` |

### Claim Stubs Written

None. The one real gap found (no media-consumption/doomscrolling angle, no relationship-ratio angle) isn't a specific missing claim—it's a direction for future capture, not a stub-worthy proposition yet.

### No evidence / needs your call

| Candidate | Why untestable |
|---|---|
| None | All candidates were testable; verdicts stand as above. |

---

### Validation

- `edge_lint.py`: not yet run—no edges written this pass (Part 1 is proposal-only per this prompt's checkpoint).
- Confidence: **high** on the one Patch A edge (explicit textual dependency in the SoT); **medium-high** on the four Patch B links (genuinely related, evidenced via the SoT's own prose or the candidate note's own content, but none pass strict Load); **medium** on the MoC anchor (a real gap in the MOC's taxonomy, but naming the new subsection is a judgment call, not a fact).

---

## Next action

~~Leon: confirm which of Patch A/B/C to apply.~~ **Applied 2026-09-10** — Leon confirmed "yes." All three patches written; validation clean (see Part 3 below). [[SoT - The Negativity Bias]]'s two broken links (`[[Humans Are Social Creatures]]`, `[[Why External Validation is So Powerful]]`) remain untouched, still flagged for a future pass.

---

## PART 3 — Thread Audit (Target Seed) — 2026-09-10

### Verdict

Target now has a real, tested position in the graph: one typed `depends_on` edge (written on the dependent's file, `SoT - The Negativity Bias`), four untyped `## Related` links on itself, one new MoC subsection anchoring it into `MOC - Cognitive Biases`, and conformant ConceptNote frontmatter. It went from "thin" (2 inbound, 0 outbound, no reciprocal link) to a genuinely two-way-navigable node without any fabricated dependency—every Patch B link stayed untyped because none passed Load-testing in Part 1.

### Exposure List

- **Dependents (things that `depends_on`/`supports` this note):** 1 — `SoT - The Negativity Bias`. This is real: retracting the Target's claim would collapse that SoT's §3–§5.
- **Dependencies (things this note `depends_on`/`supports`):** 0 — the Target itself is a root/axiom-shaped concept; nothing it asserts rests on another vault claim.
- The four Related links and the MoC anchor don't count toward exposure (untyped/structural, per the compiler's own rule)—correctly so, since none passed Load-testing.

### Threads

- **Thread 1 (Negativity Bias → SoT - The Negativity Bias):** root = `Negativity Bias` (concept, now effectively axiom-shaped—nothing grounds it further up, nothing needs to), chain = the one `depends_on` edge, tip = the SoT's applied ADHD framework. Weakest link: the Target's own claim itself, since it's the base of the chain and carries no upstream support in this vault (it's presented as established psychology, not argued from vault-internal premises)—cheapest defeater would be evidence that the "evolutionary leftover" framing is empirically contested, which the vault doesn't currently carry either way.
- **Thread 2 (topical cluster, no typed edges):** Loss Aversion / Prospect Theory / Cognitive Reframing of Criticism / Distorted Negative Self-Image — four independent leaves, discoverable now via the Target's `## Related`, correctly not treated as a justification chain.

### Traversal Manifest

- **Inbound:** 1 typed (`SoT - The Negativity Bias` `depends_on` Target), 1 remaining untyped inbound (`MOC - Why Thoughts Feel More Important When Thinking Them`, unchanged from Part 1—not tested this pass, out of scope).
- **Outbound:** 4 untyped `[[wikilink]]`s (Patch B), 0 typed edges from the Target itself (correctly—see Part 1 verdicts).
- **Termination class:** immediate on both sides; no multi-hop chain beyond the one typed edge.

### Use-vs-Mention Re-classification (post-patch)

| Link | Classification | Basis |
|---|---|---|
| [[SoT - The Negativity Bias]] | Use (typed, on the SoT's side) | Explicit `depends_on` edge, textually grounded. |
| [[Loss Aversion Describes Asymmetric Pain of Loss vs Pleasure of Gain]] | Mention | Confirmed independent evidentiary basis (Kahneman/Tversky)—correctly left untyped. |
| [[Cognitive Reframing of Criticism]] | Mention | Self-justifying procedure; doesn't invoke this bias by name. |
| [[Distorted Negative Self-Image]] | Mention | Stands as its own claim about ambiguous-feedback interpretation. |
| [[MOC - Cognitive Biases]] | Navigational (MoC membership) | Correctly untyped per the typed-edge spec's own rule. |

No candidate was upgraded on re-test; Part 1's verdicts hold.

### Denial/Substitution/Load Re-test

Unchanged from Part 1 for all four Patch B links—none promoted to Patch A.

### Structural Pathologies Found

- **Resolved:** the Target was reciprocally under-linked despite having a real, textually-grounded parent. Fixed.
- **Still open, not this note's problem:** `SoT - The Negativity Bias` carries two of its own broken links (`Humans Are Social Creatures`, `Why External Validation is So Powerful`)—confirmed absent under both filename and alias search. Candidate for a future single-note refresh on the SoT itself.
- **Vault coverage gap, unchanged from Part 1:** no media-consumption/doomscrolling or relationship-ratio (Gottman/Losada) angle on this bias exists anywhere in the vault.

### Patch A (Typings)

Applied — see above. No further typings surfaced on re-test.

### Patch B (Sever Candidates / Mergers)

None. Nothing written this pass needs severing.

### No evidence / needs your call

| Candidate | Why untestable |
|---|---|
| None this pass | All candidates were testable in Part 1; verdicts stand. |

### Frontier

- `SoT - The Negativity Bias`'s two broken links are the natural next single-note refresh in this cluster.
- If a media-consumption or relationship-ratio note is ever captured, it has a clear, well-grounded home to link back to now.

### Validation

- `edge_lint.py --audit`: 0 new errors (2 pre-existing, unrelated, unchanged); gap count unchanged (5); the new `depends_on` edge confirmed live via `--why "SoT - The Negativity Bias"`.
- Confidence: high.

### Next Action

None required—Target is now conformant, positioned under a real (not fabricated) dependency, discoverable via four verified topical links across distinct contexts (ADHD/psychology, behavioral economics, practical self-development, parenting), and anchored in the cognitive-bias taxonomy MoC. Close this audit.
