---
type: link_report
status: tmp
source_atoms: '[[tmp_atoms_pkm-meta-graph-system-research]]'
created_utc: '2026-09-13T00:00:00Z'
permalink: llmeon/00-inbox/link-report-pkm-meta-graph-system-research
---

### Link Report: A Portable Interest and PKM Knowledge Graph

#### Summary

- Atoms processed: 13
- Notes created: 13
- Total links made: 21 (7 as machine-readable typed edges; the rest as annotated `[[wikilinks]]` under Related/Tensions/See Also, per the semantic-connection lenses)
- Unlinked atoms (no connections found): 1

#### Link Map

| Atom | Links | Strongest Connection |
|------|-------|---------------------|
| [[The Collector's Fallacy Conflates Gathering with Assimilation]] | 3 | [[SoT - Illusion of Explanatory Depth (IoED)]]—direct concept match, typed `extends` |
| [[Sweller's Three Cognitive Load Types Must Be Balanced in Any Knowledge System]] | 1 | [[Cognitive Load]]—direct concept match, typed `extends` |
| [[Sensemaking Proceeds Through Generation, Data-Coverage, and Representational-Shift Loops]] | 1 | [[Comprehension Requires Passing Through a Period of Disorientation]]—shared mechanism |
| [[Feynman's Twelve Favorite Problems Acts as a Continuous Curiosity Filter]] | 3 | [[SoT - Active Learning Techniques]]—extends the canonical antidote list |
| [[Conceptual Blending Integrates Two Domains Through Four Mental Spaces]] | 0 | (none) |
| [[Conceptual Integration Networks Have Four Typologies Distinguished by Shared Framing]] | 1 | [[Conceptual Blending Integrates Two Domains Through Four Mental Spaces]]—typed `extends` (sibling atom from this same batch) |
| [[Ranganathan's PMEST Facets Decompose a Subject Without Forcing a Single Parent Category]] | 1 | [[A Faceted PKM Schema Should Separate Domain (Visible Subject) from Theme (Cross-Cutting Mechanism)]]—sibling atom, reverse-direction `extends` |
| [[Betweenness Centrality Identifies Interdisciplinary Bridge Concepts]] | 1 | [[HEAD - How Should Interests Stay Aligned Across Obsidian, Calibre, Todoist, Hookmark, and NotebookLM]]—applies to |
| [[A Faceted PKM Schema Should Separate Domain (Visible Subject) from Theme (Cross-Cutting Mechanism)]] | 4 | [[SoT - Canonical Interest Tags]]—applies to this session's own ADHD-pilot edge case (no BookFusion Shelf exists for ADHD), typed `extends` to [[Ranganathan's PMEST Facets Decompose a Subject Without Forcing a Single Parent Category]] |
| [[A Proposed Eight-Predicate Edge Vocabulary for Typed PKM Links]] | 1 | [[SoT - Typed Edge Vocabulary (Knowledge Graph Relations)]]—genuine typed `contradicts`: only `supports` overlaps between the two vocabularies |
| [[Equating Semantic Similarity with Knowledge Is a PKM Anti-Pattern]] | 1 | [[SoT - Canonical Interest Tags]]—applies to Archilles' similarity-search tools documented there |
| [[A Beautiful Global Graph View Is Not Evidence of a Better PKM System]] | 1 | [[Network Graph Views Can Induce Apophenia Through Software-Drawn Connections]]—shared mechanism (sibling atom) |
| [[Network Graph Views Can Induce Apophenia Through Software-Drawn Connections]] | 3 | [[Apophenia is the Tendency to Perceive Patterns in Random Data]]—direct concept match, typed `extends` |

#### Orphan Atoms (No Links Found)

- [[Conceptual Blending Integrates Two Domains Through Four Mental Spaces]]—no existing vault note covers conceptual blending theory or Fauconnier/Turner; may connect once other synthesis-theory notes exist, or once its sibling atom on integration-network typologies is itself linked from elsewhere.

#### Note on Typed Edges

Beyond the semantic-connection-protocol's standard `[[wikilink]] + prose annotation` links, 7 of the above connections were also written as machine-readable typed edges (`[relationship:: [[target]]]`) per the vault's [[SoT - Typed Edge Vocabulary (Knowledge Graph Relations)]], since the user's task explicitly asked for typed edges: 6 `extends` and 1 `contradicts`. Validated with `edge_lint.py --path .`: 0 new errors (2 pre-existing, unrelated errors elsewhere in the vault are untouched). The `contradicts` edge on [[A Proposed Eight-Predicate Edge Vocabulary for Typed PKM Links]] is the most significant finding of this batch — the research's proposed edge vocabulary genuinely conflicts with the vault's own closed six-relation vocabulary and cannot be adopted without a deliberate decision to extend it.