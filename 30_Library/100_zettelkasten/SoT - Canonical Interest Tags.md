---
aliases: [Cross-Tool Interest Tags, Interest Vocabulary]
conformant: true
created: 2026-09-13T00:00:00+00:00
modified: 2026-11-13T12:41:00+00:00
permalink: llmeon/30-library/so-t/so-t-canonical-interest-tags
see_also:
  - "[[Reference - Vault Interest Map]]"
  - "[[Meta MOC - The Core Domains]]"
status: stable
tags: [domain/pkm, topic/knowledge-architecture, topic/tooling]
title: SoT - Canonical Interest Tags
type: sot
---

## Minimum Viable Understanding (MVU)

This is the Rosetta Stone for cross-tool interest alignment: one row per interest node from [[Reference - Vault Interest Map]], mapping that node's canonical Obsidian tag/hub to its Calibre-side representation (Tag and/or BookFusion Shelf), Hookmark tag, and Archilles search-interest keyword.

It operates at the hub level—one row per core interest (there are 12), not per note or per book: a shared vocabulary lets you stand in any tool and find the matching content in the others, without a sync engine forcing all tools into one taxonomy.

Only ADHD is piloted so far. The other 11 rows are stubs until the ADHD pilot proves the pattern is worth repeating eleven more times. Todoist is explicitly out of scope for this vocabulary (decided 2026-09-13)—no Todoist column exists here and none should be added without reopening that decision.

---

## 1. Piloted: ADHD & Executive Function

| Layer | Value | Notes |
|:---|:---|:---|
| Obsidian tag | `TheHuman/Health/ADHD` | Canonical as of the 2026-09-13 cleanup (229 notes in `30_Library/100_zettelkasten`). Four qualifier tags (`adhd-tools`, `adhd-friendly`, `adhd-optimization`, `adhd-self-compassion`) are deliberately separate—they describe a _quality_ of something else, not "this note is about ADHD," and should not be merged into the canonical tag. |
| Obsidian hub | [[MOC - ADHD (The Master Map)]] | Plus five sub-MOCs: [[MOC - ADHD Hyperfixation-Burnout Cycle]], [[MOC - ADHD Functional Neurology & Scaffolding]], [[MOC - ADHD Project Continuation Challenge]], [[MOC - ADHD Experiments & Protocols]], [[MOC - ADHD and PKM Systems]]. |
| Calibre Tag | `ADHD` | 10 books. |
| BookFusion Shelf | _(none)_ | Edge case that broke the Phase 2 "Shelf=broad, Tag=fine" rule: ADHD has no shelf of its own—its books scatter across `Mindfulness`, `Productivity`, and `Family` depending on content. For this node, Calibre Tag is the anchor, not Shelf. Don't assume every future row will have a shelf. |
| Archilles keyword | `ADHD` (proposed, not yet set) | Would be set via the `set_research_interests` MCP tool once Archilles finishes its initial index—not done yet, since indexing was still running when this row was written. Boosts matching results in `search_books_with_citations`/`search_annotations` ranking without re-indexing. |
| Hookmark | Seeded 2026-09-13 (14 bookmarks) | Created a `MOC - ADHD (The Master Map)` bookmark (`obsidian://adv-uri`) and an `ADHD 2.0` Calibre bookmark (`calibre://show-book/DAL/695`), hooked them together, and tagged all 14 ADHD-matching bookmarks (12 pre-existing Google Docs + 2 new ones) with Hookmark's native `ADHD` tag (`bookmarks with tags {"ADHD"}`). Remaining limitation: Calibre has no predictable URL for "search by tag," so the Calibre side still points at one representative book. |
| Hookmark tag | `ADHD` (native Hookmark tag, seeded 2026-09-13, 14 bookmarks) | Query via `bookmarks with tags {"ADHD"}` in any Hookmark AppleScript context. |
| NotebookLM | None identified yet | No dedicated ADHD notebook found during the tool review. Would need to be created and referenced by URL manually—no API exists to discover this automatically (see [[SoT - Tool - NotebookLM]]). |

---

## 2. Stubs: the Remaining 11 Core Interests

Not yet audited or piloted. Listed here so the table's shape is visible alongside the current Obsidian hubs; populating any of these ahead of the ADHD pilot proving out would undercut the point of piloting. Where a Calibre-side candidate is visible from [[Main Topics of Interest]], it is noted as an unconfirmed hint, not a decision.

| Interest Node (per [[Reference - Vault Interest Map]]) | Obsidian Hub Hint | Unconfirmed Calibre-side Hint |
|:---|:---|:---|
| Knowledge management (PKM) & ProdOS | [[MOC - ProdOS]] | `PKM` shelf exists; tag overlap not yet checked |
| Productivity systems & behavioural design | [[MOC - Action Management]] | `Productivity` shelf exists; heavy overlap with the ADHD row |
| Cloud infrastructure, Kubernetes & clinical data | [[MOC - Data-Centric Infrastructure & Networking (Triage)]] | Likely spans `Platform` shelf + `Kubernetes`/`Cloud Native`/`GitOps`/`Networking & Security` tags |
| AI & agentic engineering | [[SoT - Agentic AI Design Patterns]] | No dedicated shelf seen in the current 21—may be another ADHD-shaped edge case |
| Philosophy, epistemology & thought/language | [[MOC - How Can I Know Something]] | `Philosophy` shelf exists |
| Mathematics foundations & physics | [[MOC - What is Maths]] | `Maths` shelf exists |
| Software design philosophy | [[MOC - Data-Centric Software Engineering]] | Likely overlaps `Development`/`SDLC` shelves—same "too broad alone" problem flagged in [[Main Topics of Interest]] |
| Family, relationships & parenting | [[MOC - Relational Dynamics & Family (Triage)]] | `Family` shelf exists |
| Physical health, movement & embodied craft | [[MOC - Health and Vitality]] | `Health & Endurance` shelf exists |
| Psychology & social dynamics | [[MOC - Cognitive Biases]] | No dedicated shelf seen; likely tag-only like ADHD |
| Culture, aesthetics & storytelling | [[MOC - Storytelling Techniques]] | Too heterogeneous for one shelf or tag—may not fit this vocabulary's hub-level model at all |

---

## 3. Tensions & Gaps

- The "Shelf=broad, Tag=fine" rule from Phase 2 of the Calibre reconciliation is not universal—ADHD already disproves it, and the stub table above flags AI/agentic and Psychology as likely to do the same. This vocabulary should record the anchor actually used per node, not assume Shelf always exists.
- Archilles' `set_research_interests` keyword for ADHD is proposed but not yet actually set—this row is not fully live until that call is made.
- No mechanism exists yet to keep this SoT in sync if the underlying Calibre tag/shelf vocabulary changes again (same open question [[Main Topics of Interest]] raised about needing to be regenerated after every Calibre reconciliation pass).

---

## 4. Related

- [[Reference - Vault Interest Map]]—the source ranking and updated descriptions for the 12 interest nodes.
- [[Meta MOC - The Core Domains]]—top-level domain map aligned with these 12 interest clusters.
- [[Main Topics of Interest]]—the Calibre-side Shelf/Tag listing this SoT's Calibre columns are drawn from.
- [[MOC - ADHD (The Master Map)]]—the piloted node's Obsidian hub.
- [[SoT - Tool - NotebookLM]]—why the NotebookLM column can only ever be a manual reference.

[implements:: [[Reference - Vault Interest Map]], strength=4, confidence=high]
