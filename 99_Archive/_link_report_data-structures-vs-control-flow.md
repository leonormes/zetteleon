---
created_utc: 2026-09-19 00:00:00+00:00
source_atoms: '[[tmp_atoms_data-structures-vs-control-flow]]'
status: tmp
type: link_report
permalink: llmeon/00-inbox/link-report-data-structures-vs-control-flow
---

### Link Report: The Conservation of Software Complexity: The Dichotomy of Data Structures and Control Flow

#### Summary

- Atoms processed: 21
- Notes created: 21
- Total links made: 46 (Related/Direct/Extends + Tensions + See Also, excluding Further Reading)
- Personal library citations added: 8 (across 5 atoms)
- Unlinked atoms (no connections found): 0 — every atom got at least one vault link; two (009, 013) only got a weak `See Also` tag-cluster link, no direct match existing in the vault.

The vault already contains a dense, pre-existing SoT cluster on this exact topic (`SoT - Conservation of Complexity`, `SoT - The Data-Centric Philosophy`, `SoT - Type-Driven Development (The Torvalds Loop)`, `SoT - Data-Oriented Design`, `SoT - Mechanical Sympathy`, `SoT - LLM Reasoning Obeys the Complexity Conservation Law`, `SoT - Git`, `SoT - Stringly Typed vs Strongly Typed`, `SoT - Structure is Truth is a Unifying Axiom Across Formal Systems`, `SoT - Infrastructure Complexity`, `SoT - Accidental Social Complexity`, `SoT - Simple Made Easy (Rich Hickey)`), so most atoms link primarily into that SoT layer rather than into `30_Library/100_zettelkasten/`, per the instruction to prefer a genuinely direct match over forcing a zettelkasten-only link.

#### Link Map

| Atom | Links | Strongest Connection |
|------|-------|---------------------|
| [[Tesler's Law of Conservation of Complexity (Scoped)]] | 3 | [[SoT - Conservation of Complexity]] — direct concept match |
| [[Essential vs Accidental Complexity (Brooks)]] | 2 | [[SoT - Infrastructure Complexity]] — direct concept match |
| [[Mutable State Causes Combinatorial State-Space Explosion and Contaminates Pure Logic]] | 1 | [[SoT - Simple Made Easy (Rich Hickey)]] — shared mechanism |
| [[Smart Data Structures Yield Trivial Code (Torvalds' Maxim, Corrected Sourcing)]] | 2 | [[SoT - Conservation of Complexity]] — corrects unattributed quote |
| [[The Linked-List Good Taste Example Eliminates Complexity Rather Than Relocating It]] | 3 | [[Software Complexity is Conserved Between Control Flow and Representation]] — **Tension** |
| [[Git's Content-Addressed Object Store Absorbs Distributed-Trust Complexity Into Structure]] | 2 | [[SoT - Git]] — direct concept match |
| [[Rob Pike's Rule 5 - Data Dominates]] | 2 | [[SoT - The Data-Centric Philosophy]] — direct concept match |
| [[Corrected Quote Lineage - Brooks, Pike, Raymond, Torvalds (Fold Knowledge Into Data)]] | 3 | [[SoT - The Data-Centric Philosophy]] — extends its attribution table |
| [[Cyclomatic Complexity Is a Lagging Symptom of Poor Data Modelling, Not the Root Cause]] | 1 | [[SoT - Conservation of Complexity]] — weak tag-cluster only |
| [[Shotgun Parsing Scatters Validation Logic Through Execution Logic]] | 1 | [[SoT - Type-Driven Development (The Torvalds Loop)]] — direct concept match |
| [[Parse, Don't Validate - Validation Is Lossy, Parsing Is Constructive]] | 1 | [[SoT - Type-Driven Development (The Torvalds Loop)]] — direct concept match |
| [[Making Illegal States Unrepresentable via Types (NonEmpty List Example)]] | 2 | [[SoT - Type-Driven Development (The Torvalds Loop)]] — direct concept match |
| [[Jackson Structured Programming - Control Flow Should Be Isomorphic to Data Structure]] | 1 | [[SoT - Type-Driven Development (The Torvalds Loop)]] — weak tag-cluster only |
| [[Structure-of-Arrays Eliminates the Cache-Miss Stalls Array-of-Structures Causes]] | 3 | [[SoT - Data-Oriented Design]] — direct concept match |
| [[Primitive Obsession Forces Validation Into Control Flow, Value Objects Absorb It Into Structure]] | 2 | [[SoT - Stringly Typed vs Strongly Typed]] — direct concept match (shares its aliases) |
| [[Poor Data Structure Exhausts an AI Coding Agent's Context Window Before It Can Trace Execution Logic]] | 1 | [[SoT - LLM Reasoning Obeys the Complexity Conservation Law]] — direct concept match |
| [[Elimination and Relocation Are Distinct Complexity-Management Mechanisms, Often Conflated as Conservation]] | 4 | [[Software Complexity is Conserved Between Control Flow and Representation]] — **Tension** |
| [[A Conservation Claim Becomes Unfalsifiable If Essential Complexity Is Defined Post-Hoc]] | 3 | [[SoT - Conservation of Complexity]] — **Tension** |
| [[Moving a Constraint Into a Type Is Cost Amortisation, Not a Zero-Sum Transfer]] | 3 | [[SoT - Conservation of Complexity]] — **Tension** |
| [[The Right Data Structure, Not a Smart One, Is Pike's Actual Rule]] | 2 | [[SoT - Data-Oriented Design]] — qualifies |
| [[Empirical Support for Types Prevent Bugs Is Thin and Indirect]] | 2 | [[Software Complexity is Conserved Between Control Flow and Representation]] — qualifies |

#### Tensions Flagged Against Existing Claims

Three atoms (005, 017, 019) plus one falsifiability atom (018) carry `## Tensions` edges against both [[Software Complexity is Conserved Between Control Flow and Representation]] (zettelkasten claim) and/or [[SoT - Conservation of Complexity]] (its SoT target via the `supports:: [[SoT - Complexity Conservation]]` alias edge). All four qualify rather than flatly refute: the mechanism (structure absorbs complexity) survives; the specific claim that total complexity is a strict zero-sum invariant does not — the source material's own linked-list "good taste" example is a structural counterexample (elimination, not relocation), and the strongest defensible version of the thesis is "structure is a cheaper home for complexity," not "complexity is conserved."

#### Orphan Atoms (No Links Found)

None. Weakest links: Atom 009 (cyclomatic vs data complexity) and Atom 013 (Jackson Structured Programming) — no existing vault note covers either topic directly; both got only a `See Also` tag-cluster link and may warrant becoming the seed of new SoT coverage if this cluster gets worked further.

#### Observation (Out of Scope, Not Fixed)

The existing claim note `Software Complexity is Conserved Between Control Flow and Representation.md` itself contains a dangling link — `source:: [[Code vs Data Structures (Torvalds Essay)]]` — pointing at an essay that, per this atomisation's own Atom 004, does not exist. Also pre-existing and unrelated to this batch: `[[SoT - Parse, Don't Validate]]` is referenced (broken) from three other SoT/MoC notes (`SoT - Error Handling Architecture`, `MOC - Software Architecture Principles`, `MOC - Type Theory`, `SoT - The Infrastructure Witness Pattern`) — none of my new atom notes touch or introduce this link; flagging only because `Parse, Don't Validate - Validation Is Lossy, Parsing Is Constructive.md` (this batch) is content-adjacent and could be the natural target for a future rename/redirect, at human discretion.