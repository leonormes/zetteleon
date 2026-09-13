---
conformant: true
created: 2026-09-13T09:35:01+00:00
created_utc: '2026-09-13T00:00:00Z'
modified: 2026-09-13T09:36:16+00:00
permalink: llmeon/00-inbox/a-faceted-pkm-schema-should-separate-domain-visible-subject-from-theme-cross-cutting-mechanism
source_title: A Portable Interest and PKM Knowledge Graph
source_url: UNKNOWN
status: seed
tags: [domain, faceted-classification, pkm, taxonomy, theme]
title: A Faceted PKM Schema Should Separate Domain (Visible Subject) from Theme (Cross-Cutting Mechanism)
  Mechanism)
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

### Related

[extends:: [[Ranganathan's PMEST Facets Decompose a Subject Without Forcing a Single Parent Category]], strength=3, confidence=medium]

- [[Ranganathan's PMEST Facets Decompose a Subject Without Forcing a Single Parent Category]]—extends: this domain/theme split is a simplified, two-facet special case of the fuller five-facet PMEST model.
- [[SoT - Canonical Interest Tags]]—applies to: that SoT already hit exactly this domain/theme ambiguity in its ADHD pilot row (no BookFusion Shelf exists for ADHD; Calibre Tag had to be the anchor instead), without yet having this general principle to explain why. This note's "promote only after 3+ domains" rule gives that project a concrete test for whether a candidate Calibre Shelf or Obsidian tag deserves theme status.
- [[Reference - Vault Interest Map]]—applies to: the 12 "core interests" ranked there are functioning as domains in this note's sense; the map's own cross-cutting observations (e.g. ADHD "closely fused with" productivity systems) are early evidence of un-formalised themes.

### See Also

- [[HEAD - How Should Interests Stay Aligned Across Obsidian, Calibre, Todoist, Hookmark, and NotebookLM]]
