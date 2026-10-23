---
conformant: true
contradicts: []
created: 2026-09-13T09:35:01+00:00
created_utc: '2026-09-13T00:00:00Z'
epistemic_status: medium
evidence_links: []
modified: 2026-10-22T15:11:19+00:00
permalink: llmeon/00-inbox/a-faceted-pkm-schema-should-separate-domain-visible-subject-from-theme-cross-cutting-mechanism
proposition: A faceted PKM schema should record the visible subject area of a note as its domain and a cross-cutting mechanism or question as its theme, and should promote a term to a theme only once it repeatedly links at least three distinct domains.
source_title: A Portable Interest and PKM Knowledge Graph
source_url: UNKNOWN
status: seed
tags: [domain, faceted-classification, pkm, taxonomy, theme]
title: A Faceted PKM Schema Should Separate Domain (Visible Subject) from Theme (Cross-Cutting Mechanism)
type: claim
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
- Later work found the two-facet split insufficient and vault-content theme detection biased; both have their own notes below.

### Related

[extends:: [[Ranganathan's PMEST Facets Decompose a Subject Without Forcing a Single Parent Category]], strength=3, confidence=medium]

- [[Ranganathan's PMEST Facets Decompose a Subject Without Forcing a Single Parent Category]]—extends: this domain/theme split is a simplified, two-facet special case of the fuller five-facet PMEST model.
- [[SoT - Canonical Interest Tags]]—applies to: that SoT already hit exactly this domain/theme ambiguity in its ADHD pilot row in its ADHD pilot row; the 3+ domain rule gives it a test for whether a candidate tag deserves theme status.
- [[Reference - Vault Interest Map]]—applies to: its 12 core interests function as domains, and its cross-cutting observations are early, unformalised themes.
- [[A Drive Explains Why a Domain Holds Attention and Is a Different Kind of Node From a Theme]]—extended by: adds a third facet, the drive, which explains why a domain holds attention and must not be conflated with a theme.
- [[Running the Three-Domain Rule on Two Live Candidates Cleared One and Correctly Withheld the Other]]—tested by: the promotion rule run on two live candidates, one cleared and one correctly withheld.
- [[Scoring Candidate Themes by Vault Content Is a Biased Detector Because Off-Vault and Unrecorded Engagement Leaves No Trace]]—limited by: the failure mode of detecting themes from vault content alone.

### See Also
