---
aliases: [Cross-Tool Interest Tags, Interest Vocabulary]
conformant: true
created: 2026-09-13T00:00:00+00:00
modified: 2026-09-19T15:45:17+00:00
permalink: llmeon/30-library/so-t/so-t-canonical-interest-tags
tags: [domain/pkm, topic/knowledge-architecture, topic/tooling]
title: SoT - Canonical Interest Tags
type: sot
---

## Minimum Viable Understanding (MVU)

This is the Rosetta Stone for [[HEAD - How Should Interests Stay Aligned Across Obsidian, Calibre, Todoist, Hookmark, and NotebookLM]]: one row per interest node from [[Reference - Vault Interest Map]], mapping that node's canonical Obsidian tag/hub to its Calibre-side representation (Tag and/or BookFusion Shelf) and its Archilles search-interest keyword.

It operates at the hub level—one row per core interest (there are 12), not per note or per book—per the Option A architecture in the HEAD note: a shared vocabulary is what lets you stand in any tool and find the matching content in the others, without a sync engine forcing all tools into one taxonomy.

Only ADHD is piloted so far. The other 11 rows are stubs. Per the HEAD note's plan, they stay stubs until the ADHD pilot proves the pattern is worth repeating eleven more times—see that note before populating any of them.

Todoist is explicitly out of scope for this vocabulary (decided 2026-09-13)—no Todoist column exists here and none should be added without reopening that decision.

---

## 1. Piloted: ADHD & Executive Function

| Layer | Value | Notes |
|:---|:---|:---|
| Obsidian tag | `TheHuman/Health/ADHD` | Canonical as of the 2026-09-13 cleanup—223 notes, zero duplicate variants remaining. Four qualifier tags (`adhd-tools`, `adhd-friendly`, `adhd-optimization`, `adhd-self-compassion`) are deliberately separate—they describe a _quality_ of something else, not "this note is about ADHD," and should not be merged into the canonical tag. |
| Obsidian hub | [[MOC - ADHD (The Master Map)]] | Plus five sub-MOCs: [[MOC - ADHD Hyperfixation-Burnout Cycle]], [[MOC - ADHD Functional Neurology & Scaffolding]], [[MOC - ADHD Project Continuation Challenge]], [[MOC - ADHD Experiments & Protocols]], [[MOC - ADHD and PKM Systems]]. |
| Calibre Tag | `ADHD` | 10 books. |
| BookFusion Shelf | _(none)_ | Edge case that broke the Phase 2 "Shelf=broad, Tag=fine" rule: ADHD has no shelf of its own—its books scatter across `Mindfulness`, `Productivity`, and `Family` depending on content. For this node, Calibre Tag is the anchor, not Shelf. Don't assume every future row will have a shelf. |
| Archilles keyword | `ADHD` (proposed, not yet set) | Would be set via the `set_research_interests` MCP tool once Archilles finishes its initial index—not done yet, since indexing was still running when this row was written. Boosts matching results in `search_books_with_citations`/`search_annotations` ranking without re-indexing. |
| Hookmark | Correction to an earlier wrong assumption: Hookmark was not "barely used"—it already held 192 real bookmarks, including a cluster of 12 ADHD-related Google Docs, none of which were tagged. Once Hookmark was properly installed as a real app (2026-09-13, via chezmoi/brew cask, Pro licence activated) its real AppleScript API (`Contents/Resources/hook.sdef`) became inspectable, and the plan was executed for real: created a `MOC - ADHD (The Master Map)` bookmark (→ `obsidian://adv-uri`) and an `ADHD 2.0 (Calibre, representative ADHD-tagged book)` bookmark (→ `calibre://show-book/DAL/695`), hooked them together via the `hook` command, and verified the bidirectional link by reading `hooked bookmarks` back. Then tagged all 14 ADHD-matching bookmarks (the 12 pre-existing Google Docs + the 2 new ones) with a Hookmark-native `ADHD` tag and verified `bookmarks with tags {"ADHD"}` returns all 14. This is a fourth real cross-tool layer the original plan didn't know existed: Hookmark's own tag system, now seeded, spans Google Docs + the Obsidian MOC + the Calibre book in one query. Two earlier attempts to write plain `.hookmark` files directly into `~/Documents/Hookmark/Hookmark Files/` were confirmed not to register as real bookmarks (checked via `every bookmark whose name contains "ADHD"` before they existed in the list)—those files were deleted. Remaining limitation, unchanged: Calibre has no predictable URL for "search by tag"—it's generated live via the GUI's "Copy search as URL"—so the Calibre side still points at one representative book, not a live search over all 10 ADHD-tagged books. |
| Hookmark tag | `ADHD` (native Hookmark tag, seeded 2026-09-13, 14 bookmarks) | New layer, not in the original plan. Query via `bookmarks with tags {"ADHD"}` in any Hookmark AppleScript context. |
| NotebookLM | None identified yet | No dedicated ADHD notebook found during the tool review. Would need to be created and referenced by URL manually—no API exists to discover this automatically (see [[SoT - Tool - NotebookLM]]). |

---

## 2. Stubs: the Remaining 11 Core Interests

Not yet audited or piloted. Listed here only so the table's shape is visible; populating any of these ahead of the ADHD pilot proving out would undercut the point of piloting. Where a Calibre-side candidate is already visible from [[Main Topics of Interest]], it's noted as an unconfirmed hint, not a decision.

| Interest Node (per [[Reference - Vault Interest Map]] ranking) | Unconfirmed Calibre-side hint |
|:---|:---|
| Cloud infrastructure & Kubernetes | Likely spans `Platform` shelf + `Kubernetes`/`Cloud Native`/`GitOps`/`Networking & Security` tags |
| Knowledge management itself (PKM) | `PKM` shelf exists; tag overlap not yet checked |
| Productivity systems & behavioural design | `Productivity` shelf exists; heavy overlap with the ADHD row already observed |
| AI & agentic engineering | No dedicated shelf seen in the current 21—may be another ADHD-shaped edge case |
| Philosophy & epistemology | `Philosophy` shelf exists |
| Mathematics foundations | `Maths` shelf exists |
| Software design philosophy | Likely overlaps `Development`/`SDLC` shelves—same "too broad alone" problem flagged for Development in [[Main Topics of Interest]] |
| Family, relationships & parenting | `Family` shelf exists |
| Physical health & movement | `Health & Endurance` shelf exists |
| Psychology & social dynamics | No dedicated shelf seen; likely tag-only like ADHD |
| Lighter threads (cyberpunk, fables, photography, wabi-sabi, physics) | Too heterogeneous for one shelf or tag—may not fit this vocabulary's hub-level model at all |

---

## Tensions & Gaps

- The "Shelf=broad, Tag=fine" rule from Phase 2 of the Calibre reconciliation is not universal—ADHD already disproves it, and the stub table above flags AI/agentic and Psychology as likely to do the same. This vocabulary should record the anchor actually used per node, not assume Shelf always exists.
- Archilles' `set_research_interests` keyword for ADHD is proposed but not yet actually set—this row is not fully live until that call is made.
- No mechanism exists yet to keep this SoT in sync if the underlying Calibre tag/shelf vocabulary changes again (same open question [[Main Topics of Interest]] raised about needing to be regenerated after every Calibre reconciliation pass).

## Related

- [[HEAD - How Should Interests Stay Aligned Across Obsidian, Calibre, Todoist, Hookmark, and NotebookLM]]—the plan this SoT operationalizes.
- [[Reference - Vault Interest Map]]—the source ranking for the 12 interest nodes.
- [[Main Topics of Interest]]—the Calibre-side Shelf/Tag listing this SoT's Calibre columns are drawn from.
- [[MOC - ADHD (The Master Map)]]—the piloted node's Obsidian hub.
- [[SoT - Tool - NotebookLM]]—why the NotebookLM column can only ever be a manual reference.
