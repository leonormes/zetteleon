---
conformant: false
created: 2026-09-13T09:35:01+00:00
created_utc: '2026-09-13T00:00:00Z'
modified: 2026-09-26T08:45:25+00:00
non_conformance_reason: "missing schema field definition for type concept (required when conformant - true); missing schema field distinguishes_from for type concept (required when conformant - true); missing schema field used_in_claims for type concept (required when conformant - true)"
permalink: llmeon/00-inbox/a-faceted-pkm-schema-should-separate-domain-visible-subject-from-theme-cross-cutting-mechanism
source_title: A Portable Interest and PKM Knowledge Graph
source_url: UNKNOWN
status: seed
tags: [domain, faceted-classification, pkm, taxonomy, theme]
title: A Faceted PKM Schema Should Separate Domain (Visible Subject) from Theme (Cross-Cutting Mechanism)
type: concept
upstream: '[[PKM Meta-Graph System Research]]'
---

## A Faceted PKM Schema Should Separate Domain (Visible Subject) from Theme (Cross-Cutting Mechanism)

In a faceted PKM design, "domain" should record the visible subject area a note belongs to (e.g. archery, Kubernetes, literature), while "theme" should record a mechanism or question that cuts across domains (e.g. feedback, resilience, deliberate practice); a single note may carry several domains and up to a few themes simultaneously.

### Scope & Conditions

Themes should only be promoted from candidate terms to formal theme nodes once they repeatedly link at least three distinct domains; themes that merely duplicate a domain name should be retired or merged.

### Evidence

> "Promote a term to a theme only when it repeatedly links at least three domains. Retire or merge themes that merely duplicate domain names."

### Implications

- This is a direct, ready-to-use answer to which facet layer ("domain" vs "theme") a new PKM tag belongs on, avoiding the ambiguity of a single flat tag list.
- Applied to the LLMeon vault's existing `domain/*` and `topic/*` tag prefixes, this suggests `domain/*` already plays the domain role and `topic/*` already plays something like the theme role, but the "must bridge 3+ domains before promotion" discipline is not currently enforced.
- A theme-detection method that relies on vault content (tag co-occurrence, note volume, written reflection) is a biased sensor, not a neutral one—see the Failure Mode below, discovered by running the rule for real.

### Extension: A Third Facet (Drive), Discovered Downstream

[[A Portable Interest and PKM Knowledge Graph]] took this note's two-facet split and found it wasn't enough for its own purpose—explaining _why_ a domain holds attention, not just classifying what it's about. It adds a third facet, explicit in its own text: "A theme such as feedback may connect archery and DevOps conceptually. A drive such as competence may help explain why feedback-rich activities hold attention. Theme and drive can overlap, but they are not the same kind of node." A theme is a structural, descriptive mechanism found in the knowledge itself (this note's original sense); a drive is a hypothesised psychological explanation for why certain themes recur. Not every theme is a candidate driver, and not every candidate driver reduces to one theme—a single drive can operate through several different themes at once, and the project treats conflating them as a modelling error, not a simplification.

### Worked Example: Testing the 3+ Domain Promotion Rule

Two candidates surfaced in [[A Portable Interest and PKM Knowledge Graph — Interest Seed and Candidate Drivers]] (2026-09-15) show this note's promotion rule working correctly on live material, including a case where it correctly withholds promotion:

- First-Principles Modelling, Turned Inward and Outward—clears the bar easily: recurs across ADHD, discipline, PKM, mathematics, and archery in the vault's own writing, and per Leon's direct correction the same day, plausibly extends to cloud/DevOps, security, and LLM engineering too (evidenced through work-practice rather than vault text—see Failure Mode below). Five-plus domains, independently elicited. But it sits ambiguously across the theme/drive line this note's extension above just introduced: is it a neutral cross-cutting _mechanism_ (theme), or a psychological _explanation_ for why those domains hold attention (drive)? The Interest project currently treats it as a candidate driver, not a theme, because it purports to explain the pull, not just describe a pattern in it.
- Process/Construction Legitimises, Consumption Needs Defending—correctly does _not_ clear the bar. It was proposed on what looked like three domains (maths, PKM, music), but the music leg was retracted the same day once Leon corrected the record: the two notes it rested on were a conversation with his daughter about a topic and an unrelated note about F1 and film, not autobiography, and the real music history (serious daily practice, not consumption) contradicted the story built from vault silence. Two domains is below this note's own three-domain threshold—so per the rule stated here, this candidate stays unpromoted, which is the rule doing its job, not a gap in the evidence-gathering.

### Failure Mode: Vault-Mining Is a Biased Theme-Detector

If a candidate theme or domain is scored by how much vault content bridges it, two kinds of real engagement will be invisible to the count, not merely under-weighted:

- Off-vault outlets. A domain practised through paid work (Leon's DevOps/cloud/security case) generates its reflection through the work itself, not through vault writing—so it will read as low-engagement "content to organise" when it may be a live instance of the same theme or drive as the vault's richest domains.
- Pre-vault or otherwise unrecorded history. A domain with a real, intense past (Leon was a musician who "spent all day everyday practicing and playing and listening") can be almost entirely absent from the vault if that period predates it or was never written up—so tag-frequency or reflective-density scoring will misclassify it as thin or consumption-only, when the opposite is true.

Both failures look identical from inside the vault: near-zero co-occurrence with other domains. The only way to tell "genuinely thin" apart from "off-vault outlet" or "unrecorded history" is to ask directly rather than infer from what's written—the same elicit-before-classify discipline [[A Portable Interest and PKM Knowledge Graph]] already names as its Principle #2, now with a concrete failure case attached rather than a hypothetical one.

### Related

[extends:: [[Ranganathan's PMEST Facets Decompose a Subject Without Forcing a Single Parent Category]], strength=3, confidence=medium]

- [[Ranganathan's PMEST Facets Decompose a Subject Without Forcing a Single Parent Category]]—extends: this domain/theme split is a simplified, two-facet special case of the fuller five-facet PMEST model.
- [[SoT - Canonical Interest Tags]]—applies to: that SoT already hit exactly this domain/theme ambiguity in its ADHD pilot row (no BookFusion Shelf exists for ADHD; Calibre Tag had to be the anchor instead), without yet having this general principle to explain why. This note's "promote only after 3+ domains" rule gives that project a concrete test for whether a candidate Calibre Shelf or Obsidian tag deserves theme status.
- [[Reference - Vault Interest Map]]—applies to: the 12 "core interests" ranked there are functioning as domains in this note's sense; the map's own cross-cutting observations (e.g. ADHD "closely fused with" productivity systems) are early evidence of un-formalised themes.
- [[A Portable Interest and PKM Knowledge Graph — Interest Seed and Candidate Drivers]]—applies to: the worked example above lives here—two live candidates tested against this note's own three-domain promotion rule, one passing, one correctly failing.
- [[A Portable Interest and PKM Knowledge Graph]]—extends: adds the drive facet this note's two-facet model didn't have, per the Extension section above.

### See Also

- [[HEAD - How Should Interests Stay Aligned Across Obsidian, Calibre, Todoist, Hookmark, and NotebookLM]]
