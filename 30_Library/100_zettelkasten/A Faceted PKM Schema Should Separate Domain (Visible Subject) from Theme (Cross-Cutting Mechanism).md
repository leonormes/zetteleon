---
conformant: true
contradicts: []
created: 2026-09-13T09:35:01+00:00
created_utc: '2026-09-13T00:00:00Z'
epistemic_status: medium
evidence_links: []
modified: 2026-11-09T13:50:00+00:00
permalink: llmeon/00-inbox/a-faceted-pkm-schema-should-separate-domain-visible-subject-from-theme-cross-cutting-mechanism
proposition: A faceted PKM schema should record the visible subject area of a note as its domain and a cross-cutting mechanism or question as its theme, and should promote a term to a theme only once it repeatedly links at least three distinct domains.
source_title: A Portable Interest and PKM Knowledge Graph
source_url: UNKNOWN
status: seed
tags: [domain, faceted-classification, pkm, taxonomy, theme]
title: A Faceted PKM Schema Should Separate Domain (Visible Subject) from Theme (Cross-Cutting Mechanism)
type: claim
upstream: '[[A Portable Interest and PKM Knowledge Graph]]'
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
- Later work found the two-facet split insufficient (a third facet, the drive, was proposed) and vault-content theme detection biased; the notes recording those findings have since been removed from the vault.

### Related

[depends_on:: [[A Portable Interest and PKM Knowledge Graph]], strength=4, confidence=high]
- [[A Portable Interest and PKM Knowledge Graph]]—depends_on: the project that produced this rule; its typed interest graph is where the domain/theme split is applied. *Replaces the missing `PKM Meta-Graph System Research` source.*
[supports:: [[SoT - Canonical Interest Tags]], strength=3, confidence=medium]
- [[SoT - Canonical Interest Tags]]—supports: that SoT already hit exactly this domain/theme ambiguity in its ADHD pilot row; the 3+ domain rule gives it a test for whether a candidate tag deserves theme status.
[supports:: [[Reference - Vault Interest Map]], strength=3, confidence=medium]
- [[Reference - Vault Interest Map]]—supports: its 12 core interests function as domains, and its cross-cutting observations are early, unformalised themes.
[supports:: [[Meta MOC - The Core Domains]], strength=2, confidence=low]
- [[Meta MOC - The Core Domains]]—supports: the vault's own list of core domains; the facet that this claim says should stay separate from themes.
[supports:: [[Main Topics of Interest]], strength=2, confidence=low]
- [[Main Topics of Interest]]—supports: a flat interest list that mixes domains and themes, and so shows the ambiguity this schema removes.
[extends:: [[Betweenness Centrality Identifies Interdisciplinary Bridge Concepts]], strength=2, confidence=low]
- [[Betweenness Centrality Identifies Interdisciplinary Bridge Concepts]]—extends: betweenness is a graph-computable proxy for "links three or more domains", so it could test theme candidates mechanically.
[supports:: [[Identity Adoption in One Domain Lowers Friction for Adjacent Interests]], strength=2, confidence=low]
- [[Identity Adoption in One Domain Lowers Friction for Adjacent Interests]]—supports: shows why domains cluster; a theme is the mechanism spanning such clusters rather than any one cluster.
[supports:: [[Feynman's Twelve Favorite Problems Acts as a Continuous Curiosity Filter]], strength=2, confidence=low]
- [[Feynman's Twelve Favorite Problems Acts as a Continuous Curiosity Filter]]—supports: open questions that span life domains behave like themes, so they are a candidate source of theme terms.

Removed links (targets no longer exist outside `.trash/`): `Ranganathan's PMEST Facets…`, `A Drive Explains Why a Domain Holds Attention…`, `Running the Three-Domain Rule on Two Live Candidates…`, `Scoring Candidate Themes by Vault Content…`. The Implications bullet that cited the last three still reflects their findings, but they are no longer reachable.

### See Also

[depends_on:: [[MOC - PKM as Process vs Product]], strength=2, confidence=low]
- [[MOC - PKM as Process vs Product]]—depends_on: the wider map for PKM design decisions such as this schema choice.
