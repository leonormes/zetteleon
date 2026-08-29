---
aliases: [ADHD Heterogeneity, Unique Symptom Patterns]
conformant: false
contradicts: ["[[SoT - ADHD Neurology & Core Concepts]]"]
created: 2025-10-30T12:07:04+00:00
epistemic_status: medium
evidence_links: []
modified: 2026-08-29T09:35:57+00:00
non_conformance_reason: "evidence_links is empty. The body cites a specific network-analysis result (91.8%, 116,220 combinations) with no source note, citation, or study name — the note's entire evidential weight rests on an uncited statistic."
permalink: llmeon/30-library/100-zettelkasten/adhd-is-a-heterogeneous-condition-with-unique-symptom-patterns
proposition: ADHD presentation varies so widely between individuals that population-level generalisations about symptom profile have limited predictive value for any given person.
source: "[[MOC - ADHD (The Master Map)]]"
tags: [heterogeneity, TheHuman/Health/ADHD, TheHuman/Neuroscience]
title: ADHD is a Heterogeneous Condition with Unique Symptom Patterns
type: claim
---

> Open threads: [[HEAD - Does my ADHD SoT overstate a single architecture?]]

ADHD is a heterogeneous condition, meaning its presentation varies significantly from person to person. A network analysis study found that 91.8% of individuals with ADHD had a unique symptom pattern, with 116,220 possible combinations. This highlights that the "average ADHD patient" has limited informative value and that a one-size-fits-all approach to understanding or treating ADHD is inappropriate.

## What This Claim Does

This is not a descriptive fact about ADHD sitting alongside the others in the cluster. It is a constraint on generalisation—a claim whose job is to limit what every other ADHD note in the vault is entitled to assert. Its edges should therefore point at the notes it constrains, not at notes that merely share its subject matter.

## Constrains

- [[SoT - ADHD Neurology & Core Concepts]]—_§1.1 presents a single "Non-Standard Hardware" table as the ADHD architecture, and the protocol layer built on it inherits that universality. If 91.8% of presentations are unique, one spec sheet is a useful default rather than a description. That SoT does not currently say which it is._ (Recorded in frontmatter `contradicts` per [[SoT - Typed Edge Vocabulary (Knowledge Graph Relations)]] §2—see Refresh Log for the trade-off.)

## Supports

- [[ADHD Task Initiation is Not Universally the Hardest Symptom Due to Individual Variation]]—_The specific instance of this general claim: that note's argument is literally "ADHD is heterogeneous, therefore task initiation is not universally hardest." This claim is its premise._ %%[supports:: [[ADHD Task Initiation is Not Universally the Hardest Symptom Due to Individual Variation]], strength=5, confidence=high]%%
- [[Individual ADHD Strategy Involves a Hybrid System and Self-Compassion]]—_The practical consequence: if the average patient is uninformative, a strategy has to be constructed personally rather than adopted wholesale. Heterogeneity is the reason "hybrid" and "individual" appear in that note's title._ %%[supports:: [[Individual ADHD Strategy Involves a Hybrid System and Self-Compassion]], confidence=high]%%

## See Also—Topic-Adjacent, Not Logically Related

Kept for navigation. Neither stands in one of the six edge relationships, and typing them would overstate the connection.

- [[ADHD as Neurodiversity Not Deficit]]—_Previously annotated here as "provides the conceptual shift… embracing the individual variation described in the Target." That reads as a logical relation but is not one: heterogeneity is a fact about variance, neurodiversity is a normative reframing of what variance means. A condition can be highly heterogeneous and still be a deficit; the inference does not run either way._
- [[MOC - ADHD (The Master Map)]]—_The `source` field already records this; listed for navigation only._

## Gaps

- No evidence note. The 91.8% figure and the 116,220 combinations are precise enough to be checkable and unattributed enough to be uncheckable. No study name, year, author, or sample. This is the note's load-bearing content and its weakest point—everything above depends on that statistic being real and correctly reported.
- "Unique symptom pattern" is undefined. Uniqueness across 116,220 combinations is close to arithmetically guaranteed if the combination space is large enough—with enough binary symptom dimensions, near-total uniqueness is what you would expect by construction, not a finding. Whether the study controlled for this changes what the claim is worth. UNSURE—cannot be resolved without the source.

## Refresh Log

- 2026-07-25—Relationship audit. The note previously carried two untyped `## Related` links whose annotations implied logical dependence. One ([[ADHD Task Initiation is Not Universally the Hardest Symptom Due to Individual Variation]]) turned out to be a genuine general→specific relation and is now typed `supports` at strength 5; the other ([[ADHD as Neurodiversity Not Deficit]]) was topic adjacency dressed as inference and has been demoted with the reasoning stated.
- New relation found: this claim constrains [[SoT - ADHD Neurology & Core Concepts]], a tension already recorded in prose on that note's side. Now recorded formally, from the side that actually asserts it.
- Deliberately not linked: [[Extrapolating Pathology to Normal Function Is a Hasty Generalisation]] is superficially a sibling (both concern invalid generalisation) but addresses a different inference—pathology→normal, not average→individual, in a different domain. Adding it would repeat the mistake this refresh was correcting.
- Frontmatter: backfilled the `claim` fileClass fields—`proposition`, `epistemic_status: medium` (single uncited study), `evidence_links: []`, `contradicts`. Left `conformant: false` with the empty-evidence reason; the previous reason ("Bulk inferred type. Needs review.") was stale, the type is correct.
- Trade-off, for your decision: the `contradicts` relation is in frontmatter because §2 of the Typed Edge Vocabulary prefers the frontmatter field for a claim's note→note contradiction. The cost is that `edge_lint.py` does not parse frontmatter relations (§5.1), so this conflict will not appear in `--audit`'s C3 section. Moving it to an inline `%%[contradicts:: …]%%` edge makes it compiler-visible at the price of departing from the spec's stated preference.
