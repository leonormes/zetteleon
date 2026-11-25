---
title: <% tp.file.title %>
type: sot
status: seed
created: <% tp.date.now("YYYY-MM-DDTHH:mm:ssZ") %>
modified: <% tp.date.now("YYYY-MM-DDTHH:mm:ssZ") %>
conformant: true
tags:
- prodos/sot
aliases: []
prodos:
  kind: sot
  lifecycle: seedling
  trust: working
  review:
    interval: 6 months
    last_reviewed: <% tp.date.now("YYYY-MM-DD") %>
  chronos:
    last_synthesis: <% tp.date.now("YYYY-MM-DD") %>
    synthesis_count: 0
see_also: []
permalink: llmeon/10-system/templates/template-so-t
---

> Open threads: <!-- Optional: [[HEAD - Unresolved question?]] -->

## Minimum Viable Understanding (MVU)

*(2–4 sentences summarising the core thesis, why it matters, and how the compiled propositions fit together.)*

---

## 1. Core Foundations / Premises (Claims & Concepts)

*(Optional argument-thread cue: **Premises**. Brief connective framing introducing the foundational propositions—extract standalone claims and concepts to `30_Library/100_zettelkasten/` first, then transclude their opening statements here (`![[Title#^claim]]`) rather than writing un-extracted prose assertions.)*

![[Claim Title#^claim]]

![[Concept Title#^def]]

---

## 2. Mechanisms & Procedures / Argument Thread

*(Optional argument-thread cue: **Argument Thread → Conclusions & Assumptions**. Brief connective framing showing how the premises above combine into the SoT's conclusion, what assumptions remain open, and which procedures operationalise it.)*

![[Procedure Title#^claim]]

---

## Working Knowledge & Synthesis

*(Typed edges indexing every load-bearing premise and transcluded component for `edge_lint.py` and the K-Plex Idea Compass. Use `[depends_on:: [[Claim]]]` for load-bearing premises of the argument and `[synthesizes:: [[Note]]]` for transcluded components. Replace the placeholder block below with real bullets; do not duplicate these targets in frontmatter `see_also`.)*

```markdown
- [[Claim Title]]—_Load-bearing premise for the SoT's central argument._ [depends_on:: [[Claim Title]]]
- [[Claim Title]]—_One-sentence annotation of how this claim supports the thesis._ [synthesizes:: [[Claim Title]]]
- [[Concept Title]]—_One-sentence annotation of how this concept frames the domain._ [synthesizes:: [[Concept Title]]]
- [[Procedure Title]]—_One-sentence annotation of how this procedure operationalises the thesis._ [synthesizes:: [[Procedure Title]]]
```