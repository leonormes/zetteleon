---
type: link_report
status: tmp
source_atoms: '[[tmp_atoms_political-contrast-effect]]'
created_utc: '2026-09-17T00:00:00Z'
permalink: llmeon/00-inbox/link-report-political-contrast-effect
---

### Link Report: Political Contrast Effect Research

#### Summary

- Atoms processed: 12
- Notes created: 12
- Total vault links made: 8
- Total library (archilles/Calibre) citations made: 15, across 9 atoms
- Unlinked atoms (no vault connections found): 5 (all still carry library citations except where noted)
- Atoms with no library match found (flagged, not forced): 4

#### Link Map

| Atom | Vault Links | Library Sources | Strongest Connection |
|------|-------------|------------------|---------------------|
| [[Contrast Effect in Sequential Political Judgment]] | 1 (See Also) | 3 | *Thinking, Fast and Slow* (Kahneman), Ch. 11 "Anchors" — direct match |
| [[Social Judgment Theory's Latitude Recalibration]] | 0 | 1 | *How to Be a Liberal* — Sherif's own tribalism experiments (partial match) |
| [[Inclusion-Exclusion Model of Political Benchmarking]] | 1 (See Also) | 0 (gap) | [[MOC - Cognitive Biases]] |
| [[Affective Polarization]] | 1 (extends) | 2 | *Enlightenment Now* (Pinker), Ch. 21 — partisan fandom analogy |
| [[Negative Partisanship]] | 2 (extends) | 1 | *Enlightenment Now*, Ch. 21 |
| [[Threat Perception Halo Effect on In-Group Leaders]] | 1 (shared mechanism) | 2 | *Moral Tribes* (Greene) — oxytocin/in-group favouritism |
| [[Polarization Suppresses Negativity Bias Toward In-Group Lies]] | 1 (extends) | 1 | *Enlightenment Now*, Ch. 4 — negativity bias |
| [[Voters Trade Democratic Norms for Partisan Victory]] | 0 | 1 | *Enlightenment Now*, Ch. 14 — democratic backsliding |
| [[Scandal Spillover Contagion Versus Contrast]] | 1 (shared mechanism) | 0 (gap) | [[Inclusion-Exclusion Model of Political Benchmarking]] |
| [[Collective Moral Licensing in Partisan Politics]] | 1 (shared mechanism) | 0 (gap) | [[SoT - Bonhoeffer's Theory of Functional Stupidity]] |
| [[Elite Negative Representation Strategy]] | 0 | 2 | *Data and Goliath* (Schneier) — targeted political ads |
| [[Contrast-Driven Forgiveness Erodes Policy Accountability]] | 2 (extends) | 0 (gap) | [[Voters Trade Democratic Norms for Partisan Victory]] |

#### Orphan Atoms (No Vault Links Found)

- [[Social Judgment Theory's Latitude Recalibration]] — no existing vault note covers Sherif or Social Judgment Theory by name; a natural seed for a future concept note if this domain gets developed further.
- [[Voters Trade Democratic Norms for Partisan Victory]] — no existing vault note on Svolik/democratic backsliding.
- [[Elite Negative Representation Strategy]] — no existing vault note on campaign strategy or elite political behaviour.

#### Library Gaps (No archilles Match Found)

Flagged explicitly rather than forced, per the TAC "flag insufficient context" rule:

- [[Inclusion-Exclusion Model of Political Benchmarking]] — Schwarz & Bless's specific model not found in the indexed library.
- [[Scandal Spillover Contagion Versus Contrast]] — no book found treating scandal contagion vs. contrast.
- [[Collective Moral Licensing in Partisan Politics]] — semantic search returned only general moral-philosophy hits (*The Blank Slate*, *Mastering the Core Teachings of the Buddha*, *The Big Picture*), none specifically about moral licensing; excluded as too weak to cite.
- [[Contrast-Driven Forgiveness Erodes Policy Accountability]] — synthesised systemic claim, no single-book match attempted to be forced.

#### POC Notes on the archilles Semantic Search Itself

- Ran against the live index (181,621 chunks) while the background Calibre indexing job continued in parallel—no conflicts, reads work fine concurrently with writes.
- `--mode hybrid --max-per-book 1` gave good topical diversity per query; relevance scores were uniformly low in absolute terms (0.015–0.036) even for very strong conceptual matches (e.g. Kahneman's own "Anchors" chapter for an anchoring-effect query), so **score is not a reliable strength signal on this index yet**—read the returned text, don't filter on the number.
- Strongest hits were for well-known, widely-discussed mechanisms with dedicated book chapters (anchoring, negativity bias, in-group/out-group tribalism). Weakest/no hits were for more niche academic terms lifted verbatim from the source report (Inclusion/Exclusion Model, moral licensing, Svolik's specific framing)—the library evidently doesn't contain a book that names these mechanisms directly, even though related library content exists.
- Each atom's Library Sources section states explicitly when a citation is a partial/adjacent match rather than a direct one, to avoid overclaiming the search's precision.

## Output Behaviour

PROMOTED: 12 atoms → 12 permanent notes
LINKED: 8 vault connections + 15 library citations
REPORT: 00_Inbox/_link_report_political-contrast-effect.md