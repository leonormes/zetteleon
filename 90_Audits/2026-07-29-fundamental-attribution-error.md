---
title: 2026-07-29-fundamental-attribution-error
type: note
permalink: llmeon/90-audits/2026-07-29-fundamental-attribution-error
---

# Thread audit — [[Fundamental Attribution Error]] — 2026-07-29

## Verdict

The seed is not load-bearing: zero canonical typed edges touch it anywhere in the vault, and none of its eight untyped inbound "Related" links survive Denial/Substitution/Load testing as genuine inference — FAE functions as a rhetorical touchstone ("shared mechanism") cited by habit, not a premise anything actually rests on. The weakest thread is the one candidate worth taking seriously — [[Evil Arises from Malice or Thoughtless Banality — Motivation Is Not Determinative]] — where FAE is asserted as the mechanism behind mis-attributing evil to malice, but the generalising step from interpersonal bias to historical-moral judgement is never argued. Most exposed in this neighbourhood isn't the seed itself but that same note: it carries a claimed dependency, no falsifier, and no counter-position, while FAE — despite being cited eight times — has no falsifier, no crux, and is itself flagged `non_conformance_reason: "Bulk inferred type. Needs review."`

**Before you act on Patch A:** the vocabulary this brief specifies (`supports` / `prerequisite_of` / `instance_of` / `contrasts_with` / `related_to`) does not match the vault's current canonical vocabulary. [[SoT - Typed Edge Vocabulary (Knowledge Graph Relations)]] (modified 2026-07-27 — two days ago) defines a closed, compiler-enforced list: `extends`, `synthesizes`, `implements`, `contradicts`, `supports`, `depends_on`. Only `supports` appears in both. `edge_lint.py` rejects any relationship outside its own list as a hard error, not a warning. I've used the SoT's real vocabulary below wherever a typing is discussed, and flagged the brief's stale table rather than silently reconciling the two — see Pathologies.

## Exposure list

| Note | Dependents | Falsifier? | Confidence dated | Exposure |
|---|---|---|---|---|
| [[Fundamental Attribution Error]] (seed) | 0 confirmed / 1 soft (rhetorical) | No | No dated confidence field; `non_conformance_reason` flags the note itself as unreviewed | Low-by-load, high-by-citation — see note below |
| [[Evil Arises from Malice or Thoughtless Banality — Motivation Is Not Determinative]] | 1 claimed inbound dependency (on FAE, UNDERSPECIFIED) | No | No dated confidence field | Frontier — worth its own audit run |

The formula (high dependents × low scrutiny) doesn't produce a clean number here because dependents on FAE are essentially zero once tested — it's cited, not depended on. That's the finding, not a gap in the method: a note can be mentioned constantly and still carry no load. If you want a genuine exposure ranking, [[Evil Arises from Malice or Thoughtless Banality — Motivation Is Not Determinative]] is the frontier note to seed a fresh run on — it's the only place an inferential claim on FAE was actually made.

## Threads

No thread reaches KEEP status. There is no root-to-tip chain through FAE — every candidate below terminates at SEVER or UNDERSPECIFIED before a second hop. Reported as candidates, not threads, per Phase 2b.

### Candidate 1: [[Evil Arises from Malice or Thoughtless Banality — Motivation Is Not Determinative]] → FAE — UNDERSPECIFIED

- **Evidence line:** "[[Fundamental Attribution Error]]—shared mechanism: attributing evil exclusively to malice is a direct instance of the Fundamental Attribution Error—over-weighting dispositional (character) factors while under-weighting situational and structural ones." (under `### Related`)
- **Denial:** Passes — one can hold both notes true while denying that malice-attribution specifically instantiates FAE (it could be a distinct bias, e.g. moral typecasting).
- **Substitution:** Partial pass — FAE's specific trait-vs-situation mechanism is what's doing the work, so an off-topic bias wouldn't serve. But a near-synonym (correspondence bias) would substitute without changing the argument, so this isn't a clean pass.
- **Load:** Partial — the note's core Arendtian thesis (evil has two structurally distinct sources) doesn't depend on FAE; but the specific sub-claim ("attributing evil exclusively to malice is an *error*") loses its explanatory backing if FAE isn't real.
- **Suppressed premise, named:** that the disposition-over-situation weighting FAE describes in ordinary interpersonal judgement *generalises* to historical/moral judgement of perpetrators like Eichmann. That generalisation is asserted via "is a direct instance of," never argued.
- **Confidence:** medium. Not traversed as settled.

### Candidates 2–8: analogical "shared mechanism" mentions — all SEVER

Structurally identical pattern across four notes: an explicit connective phrase ("shared mechanism") sits under a `### Related` or `## Related` heading, but describes an *analogy* between two mechanisms rather than a dependency between two claims.

| From | Evidence line | Denial | Substitution | Load | Verdict |
|---|---|---|---|---|---|
| [[The Mereological Fallacy in Neuroscience]] | "shared mechanism: mis-locating agency by projecting whole-person traits onto the wrong level." | passes | fails — any misattribution-of-agency note would serve | fails — FAE false ≠ Mereological Fallacy weakened | **SEVER**, high confidence |
| [[Split-Brain Confabulation Reveals a Post-Hoc Interpreter]] | "shared mechanism: confident causal attribution made without access to the real cause." | passes | fails — any confident-misattribution note would serve | fails | **SEVER**, high confidence |
| [[Claim - Beliefs often function as belonging cues to secure group membership rather than as truth-seeking theses]] | "shared mechanism: explains the cognitive bias of blaming the person's nature rather than situational/tribal factors" | passes | fails — generic disposition-bias framing, swappable | fails — belonging-cues claim rests on tribal-signalling evidence, not FAE | **SEVER**, medium-high confidence |
| [[Pattern Recognition in Social Cognition]] (mutual, both directions) | bare, no prose, under `### Related` (both sides) | n/a | n/a | n/a | **SEVER**, low confidence (position heuristic only) |

### Candidates 9–11: bare, no annotation — SEVER, low confidence

| From | Where it sits |
|---|---|
| [[Minds Are Like Plants - Unique Products of Genes and Environment]] | Bare bullet, `## Related`, no surrounding prose |
| [[Binary Person-Judgement Is a Cognitive Default, Not a Character Flaw]] | Bare bullet, `## Related`, no surrounding prose |
| [[A False Belief Does Not Diminish a Person's Worth]] | Bare bullet, `## Related`, no surrounding prose |

## Traversal manifest

| Node | Type | Depth | Direction | Termination |
|---|---|---|---|---|
| [[Fundamental Attribution Error]] | concept (seed) | 0 | — | — |
| [[Ambiguity in Social Cues]] | *does not exist* | 1 | outbound | **target absent** — see Pathologies |
| [[Confirmation Bias Distorts Social Perception]] | *does not exist* | 1 | outbound | **target absent** — see Pathologies |
| [[Pattern Recognition in Social Cognition]] | claim | 1 | outbound + inbound (mutual) | tip — bare link, no further inferential edges out of it toward FAE |
| [[The Mereological Fallacy in Neuroscience]] | concept | 1 | inbound | tip — SEVER |
| [[Split-Brain Confabulation Reveals a Post-Hoc Interpreter]] | claim | 1 | inbound | tip — SEVER |
| [[Minds Are Like Plants - Unique Products of Genes and Environment]] | claim | 1 | inbound | tip — SEVER |
| [[Evil Arises from Malice or Thoughtless Banality — Motivation Is Not Determinative]] | claim | 1 | inbound | tip — UNDERSPECIFIED (frontier, worth extending) |
| [[Claim - Beliefs often function as belonging cues to secure group membership rather than as truth-seeking theses]] | atom | 1 | inbound | tip — SEVER |
| [[Binary Person-Judgement Is a Cognitive Default, Not a Character Flaw]] | claim | 1 | inbound | tip — SEVER |
| [[A False Belief Does Not Diminish a Person's Worth]] | claim | 1 | inbound | tip — SEVER |
| [[MOC - Social Perception and Self-Awareness]] | map | 1 | inbound | **boundary** (Domain Hub) — see Pathologies for the `rel:: distorts` annotation it carries |
| [[_link_report_analytical_exploration_of_evil]] | link_report | 2 (via Evil Arises) | — | **attribution** — machine-generated ingest artifact (`status: tmp`), corroborates the "shared mechanism" tie was auto-proposed during a batch link pass, not hand-reasoned |

No depth-cap truncation — every branch off FAE terminates at depth 1 (tip, boundary, or absent target) or depth 2 attribution. There is nothing further to name as frontier except [[Evil Arises from Malice or Thoughtless Banality — Motivation Is Not Determinative]] itself, whose own upstream/downstream graph wasn't walked (out of scope for a seed of FAE).

## Patch A — proposed typings (high confidence only)

**None.** No candidate cleared high confidence. The one substantive candidate (Evil Arises → FAE) is UNDERSPECIFIED, not KEEP — typing a guess here would bake in an ungrounded generalisation permanently. If you supply the suppressed premise (that interpersonal FAE generalises to historical/moral perpetrator judgement) and still want it recorded, the compiler-valid form would be:

```
%%[depends_on:: [[Fundamental Attribution Error]], confidence=medium]%%
```
placed in [[Evil Arises from Malice or Thoughtless Banality — Motivation Is Not Determinative]], under the `%[relationship...` convention — not `supports`/`prerequisite_of` as this brief's vocabulary would suggest, since those aren't in the compiler's closed list.

## Patch B — sever candidates

| From | To | Reason | Evidence line |
|---|---|---|---|
| [[The Mereological Fallacy in Neuroscience]] | [[Fundamental Attribution Error]] | Fails Substitution and Load — analogy, not dependency | "shared mechanism: mis-locating agency by projecting whole-person traits onto the wrong level." |
| [[Split-Brain Confabulation Reveals a Post-Hoc Interpreter]] | [[Fundamental Attribution Error]] | Fails Substitution and Load — analogy, not dependency | "shared mechanism: confident causal attribution made without access to the real cause." |
| [[Claim - Beliefs often function as belonging cues to secure group membership rather than as truth-seeking theses]] | [[Fundamental Attribution Error]] | Fails Substitution and Load — generic disposition-bias framing | "shared mechanism: explains the cognitive bias of blaming the person's nature rather than situational/tribal factors" |
| [[Fundamental Attribution Error]] | [[Pattern Recognition in Social Cognition]] | Bare, `### Related`, no prose either direction | (no prose — bare wikilink) |
| [[Pattern Recognition in Social Cognition]] | [[Fundamental Attribution Error]] | Bare, `### Related`, no prose either direction | (no prose — bare wikilink) |
| [[Minds Are Like Plants - Unique Products of Genes and Environment]] | [[Fundamental Attribution Error]] | Bare, `## Related`, no prose | (no prose — bare wikilink) |
| [[Binary Person-Judgement Is a Cognitive Default, Not a Character Flaw]] | [[Fundamental Attribution Error]] | Bare, `## Related`, no prose | (no prose — bare wikilink) |
| [[A False Belief Does Not Diminish a Person's Worth]] | [[Fundamental Attribution Error]] | Bare, `## Related`, no prose | (no prose — bare wikilink) |

## No evidence — needs your call

| From | To | Where it sits |
|---|---|---|
| [[Fundamental Attribution Error]] | [[Ambiguity in Social Cues]] | `### Related` — target note does not exist anywhere in the vault |
| [[Fundamental Attribution Error]] | [[Confirmation Bias Distorts Social Perception]] | `### Related` — target note does not exist anywhere in the vault |

Both are explicitly tracked as planned-but-unwritten atomic notes in [[MOC - Social Perception and Self-Awareness]] (`### Atomic Note Gaps (Planned)`), so these aren't stray typos — they're aspirational links ahead of the notes they point to. Your call whether to leave them as forward-references or sever until the target notes exist.

## Pathologies found

- **Vocabulary mismatch, not a vault pathology but a brief pathology.** This audit's own vocabulary table (`supports`/`prerequisite_of`/`instance_of`/`contrasts_with`/`related_to`) doesn't match [[SoT - Typed Edge Vocabulary (Knowledge Graph Relations)]]'s current closed list (`extends`/`synthesizes`/`implements`/`contradicts`/`supports`/`depends_on`), last changed two days ago. Only `supports` is shared. Any typing proposal against this seed needs to use the SoT's list to survive `edge_lint.py`.
- **Shadow vocabulary in MoCs.** [[MOC - Social Perception and Self-Awareness]] carries a visible `rel:: distorts [[Pattern Recognition in Social Cognition]]` line against FAE. `distorts` is not in either vocabulary list, and per the SoT's own §5.1, this `rel::` form is a different grammar the compiler doesn't parse at all (~303 instances vault-wide, by the SoT's own count) — it's filing furniture inside a Domain Hub, not a checked edge, however inference-shaped it reads.
- **Bare assertion, informally.** FAE has no falsifier field, no crux, no `contrasts_with` anywhere in the vault, and its own frontmatter already flags `non_conformance_reason: "Bulk inferred type. Needs review."` — it's an unreviewed note being treated as settled background by eight other notes.
- **Citation without load.** Not one of the taxonomy's named pathologies, but worth naming anyway: FAE is invoked as a "shared mechanism" by four different notes via what reads like a templated phrase, and the batch-generated [[_link_report_analytical_exploration_of_evil]] confirms at least one of those ties (Evil Arises) was proposed by an automated linking pass rather than argued by you. That's a plausible explanation for why the phrasing repeats and why none of the four survive the three tests — they may all descend from the same LLM-generated pattern rather than four independent judgements.

## Frontier

None truncated by depth cap. The one open thread worth a dedicated run: [[Evil Arises from Malice or Thoughtless Banality — Motivation Is Not Determinative]], to see what it depends on and implies once FAE is set aside as unresolved.

## Next action

Answer the "No evidence" table's call on [[Ambiguity in Social Cues]] and [[Confirmation Bias Distorts Social Perception]]: tell me forward-reference or sever, and I'll fold that into the next pass.