---
created: 2026-09-13T00:00:00+00:00
modified: 2026-09-13T10:36:53+00:00
permalink: llmeon/20-thinking/21-workbench/head-how-should-interests-stay-aligned-across-obsidian-calibre-todoist-hookmark-and-notebook-lm
status: open
tags: [domain/pkm, topic/knowledge-architecture, topic/tooling]
title: HEAD - How Should Interests Stay Aligned Across Obsidian, Calibre, Todoist, Hookmark, and NotebookLM
  Hookmark, and NotebookLM
type: head
---

## Framing Question

How can Leon's interests—a graph, not a hierarchy, with ADHD as the dominant hub and dozens of cross-cutting sub-topics (Kubernetes, PKM theory, mathematics, philosophy, health, family)—stay visible and navigable across every tool that holds a piece of them: Obsidian (LLMeon vault), Calibre/BookFusion, Google NotebookLM, and Hookmark?

> 2026-09-13—Todoist is out of scope. Explicit call: this project does not extend to Todoist. All references below are left as a historical record of the investigation, not a live part of the plan—no Todoist label/project work will happen under this HEAD note.

The goal is not to merge these tools or force one taxonomy on all of them. It's to make it possible to stand in any one of them, on any interest, and find the related content living in the others—via a shared vocabulary and a small number of explicit links, not a new sync engine.

> Nothing here is decided. This is a workbench note—the plan below is a first pass to react to and cut down, not a spec to implement wholesale.

---

## 1. What Each Tool Actually Holds Today (As of 2026-09-13)

### Obsidian (LLMeon vault)—richest eXisting sTructure, but tWo bRidge aRtifacts aRe sTale

- [[Reference - Vault Interest Map]] already ranks the interest graph's core nodes from an LLM analysis of ~2,650 notes (2026-06-10): ADHD & executive function is the dominant theme (~90+ zettels, a dozen MoCs), then Cloud/Kubernetes, PKM itself, productivity systems, AI/agentic engineering, philosophy, mathematics, software design philosophy, family, health & endurance, psychology, and lighter threads. This is the closest thing to a canonical interest-node list that already exists—the plan below treats it as the backbone rather than inventing a new one.
- [[Main Topics of Interest]] is a prior attempt at exactly this cross-tool bridge: an Obsidian note grouping `calibre://show-book/DAL/<id>` deep links under domain headings (Platform Engineering, Network Engineering, Data-Centric Software Engineering, AI Engineering, ADHD & Cognitive Scaffolding, PKM, Data Systems, Applied Mathematics, Health & Endurance). It was last synthesized 2026-04-19 and predates this session's full Calibre tag/shelf cleanup—it's now stale and needs regenerating, not rebuilding from scratch.
- Tagging already uses a light namespacing convention in frontmatter: `domain/*` (domain/pkm, domain/llm, domain/archery), `topic/*` (topic/productivity, topic/knowledge-architecture, topic/metacognition), `TheHuman/*` (TheHuman/Health/ADHD, TheHuman/Philosophy). This is inconsistently applied (many notes use flat tags instead) but it's the one piece of cross-cutting vocabulary infrastructure that already exists natively in Obsidian frontmatter.
- ADHD alone has a dedicated MOC hierarchy: [[MOC - ADHD (The Master Map)]], plus [[MOC - ADHD Hyperfixation-Burnout Cycle]], [[MOC - ADHD Functional Neurology & Scaffolding]], [[MOC - ADHD Project Continuation Challenge]], [[MOC - ADHD Experiments & Protocols]], and [[MOC - ADHD and PKM Systems]]—a genuine hub-and-spoke sub-graph, not a flat tag.
- The vault also has a full typed-edge/justification-graph system (`extends`/`supports`/`contradicts`/etc., validated by `edge_lint.py`)—this is graph infrastructure for _claims_, and is almost certainly overkill as the direct bridge to other tools, but it's worth knowing it exists so the interest-alignment system doesn't reinvent a weaker version of it inside Obsidian itself.

### Calibre / BookFusion—just Cleaned up This Session

- 62 Title-Case native tags (fine-grained sub-topic layer) + 21 BookFusion Shelf values (broad domain layer), fully covering all 502 books, no duplicates, no lowercase junk—see this session's earlier work.
- `calibre://show-book/<library>/<id>` gives a stable deep link per book, already used by [[Main Topics of Interest]].
- BookFusion itself has no public API reachable from this machine—no CLI, no local config found. Any BookFusion-side change (e.g. retiring the old `calibre` marker tag) has to happen through its web/app UI.

### Todoist—currently GTD-context-only, no Interest Layer

- Active labels: `computer`, `question`, `home`, `waiting`, `work`, `personal`, `Rae`, `Bessie`, `Pearl`—these are GTD contexts and people, not subjects.
- Shared labels seen on tasks but absent from the personal label list: `pkm`, `hermes`, `1-Next_Action`, `2-Project`, `idea`, `needs-decision`—worth checking where these came from before building on top of them.
- An archived, favorited project "Things I want to learn" already exists—dormant precedent for exactly this kind of tracking.
- An archived project "Vault Graph" shows how Leon documents a serious PKM initiative in Todoist when he commits to one: a long, phase-numbered description linking out to source-of-truth files. Worth following that pattern's _rigor_, not necessarily its exact structure, for whatever Todoist piece this plan ends up with.
- No current project or label maps to any of the Reference - Vault Interest Map's 12 core interests.

### NotebookLM—no API, Notebook-per-topic, Manual Bridge only

- [[SoT - Tool - NotebookLM]] documents how it's used: one notebook per topic (e.g. "Kubernetes Networking"), used as a Phase-T "Thinking accelerator"—ingesting many sources into a grounded synthesis, sometimes turned into an audio overview.
- It's a Chrome web app (`~/Applications/Chrome Apps.localized/NotebookLM.app`) with no scriptable API. Any link between a NotebookLM notebook and the rest of the graph has to be a manually-maintained URL reference—there's no way to query "what notebooks exist" or "what's in them" from outside the browser.

### Hookmark—installed, Barely Used, and Better-suited to This than Expected

- Confirmed installed and working: one existing hook at `~/Documents/Hookmark/Hookmark Files/Pentest cluster.hookmark`.
- A `.hookmark` file turns out to be nothing more than a plain-text file containing one deep-link URI—the example found holds `obsidian://adv-uri?vault=…&filepath=…`. Hookmark's real mechanism (when used live, not via a saved `.hookmark` file) is a HUD that lets you select two items in any two supported apps and link them bidirectionally in its own database.
- This means Hookmark can already hold `calibre://`, `obsidian://`, and (going by its general design) `omnifocus://`/`todoist://`/`https://` links side by side—it is, functionally, already the cross-tool link layer the framing question is asking for. It's just unused.
- Its link database lives partly in `~/Documents/Hookmark/` and is also mirrored to `/Volumes/DAL/Zettelkasten/Hookmark/`—already sitting on the same volume as the vaults, which may or may not be deliberate; worth confirming with Leon rather than assuming.

### Local filesystem—no Evidence of an Existing Tagging Scheme for This

- A Finder-tag search turned up nothing related to personal interests (only work/Fitfile infrastructure assets). If there are loose files (PDFs, papers, exports) outside Calibre and outside the vault that belong to this graph, they haven't been tagged yet—this is a genuine gap, but only worth addressing if such files actually exist in volume. Not assumed to be a priority without evidence.

---

## 2. The Core Design Question This Note Hasn't Resolved

Two different architectures are both defensible, and the plan below leans toward the first without fully ruling out the second:

Option A—Shared vocabulary + Obsidian as the map, Hookmark for high-value point-to-point links.

Obsidian stays the canonical graph (it already is one). A single controlled tag vocabulary is defined once and mirrored as plain strings into every other tool that supports tagging (Calibre tags/shelves, Todoist labels). Hookmark is used sparingly—one hook or composition per _interest hub_ (e.g. the ADHD MOC), bundling links to the relevant Calibre shelf-search, Todoist project, and NotebookLM notebook—not one hook per item. Finding related content in another tool means: read the tag off the note/book/task, search for that same tag over there.

Option B—Hookmark as the connective tissue for everything.

Every individual book, note, and task that matters gets hooked directly to its counterparts. Denser, more precise, but doesn't scale to hundreds of books and thousands of notes, and turns Hookmark into infrastructure that needs maintaining rather than an occasional convenience.

Leaning towards A, reserving Hookmark for the hub level, because the vault's own interest structure is already hub-and-spoke (a dozen MOCs, not thousands of independent tags)—the hubs are the natural unit for cross-tool linking, and there are few enough of them that hand-maintaining hooks is realistic.

---

## 3. Draft Plan (Sequenced, not yet cOmmitted)

1. ✅ Done 2026-09-13—Regenerate [[Main Topics of Interest]] against the current, clean Calibre tag/shelf state (62 tags, 21 shelves, 502 books). Rebuilt mechanically (Shelf as section, Tags shown per book) instead of hand-curating the old 9 bespoke domain headings. Finding: the "Development" shelf alone is 90 books (18% of the library)—Shelf-only is too coarse on its own; the Tag layer is carrying real weight, which matters for the vocabulary design in step 2 below. A second, unplanned discovery happened in the same session: [Archilles](https://github.com/kasssandr/archilles) (a local semantic-RAG MCP server for Calibre) got installed and registered in 1MCP. It exposes 13 tools, two of which are directly relevant to this plan: `search_annotations` (semantic search over highlights/notes—a richer "find related content" surface than tags alone) and `set_research_interests` (a live keyword-boost mechanism that could be seeded straight from whatever vocabulary comes out of step 2, rather than staying a separate system). Indexing was still running when this was written—revisit once it completes.
1b. ✅ Done 2026-09-13—Obsidian ADHD tag audit and cleanup. Frontmatter-only audit (not prose mentions—an earlier prose-inclusive grep had wrongly suggested ~1868 uses) found 8 distinct variants, 232 total tag-uses: `TheHuman/Health/ADHD` (169, already the de facto majority), plus duplicates `adhd` (50), `ADHD` (3), `topic/adhd` (2)—55 notes total—and four genuinely distinct qualifier tags (`adhd-tools`, `adhd-friendly`, `adhd-optimization`, `adhd-self-compassion`, 8 uses total) that are not duplicates and were left alone. Retagged all 55 duplicate-carrying notes to `TheHuman/Health/ADHD`, correctly deduplicating the one file that already carried both forms. Re-audit confirms: `TheHuman/Health/ADHD` now 223, zero bare/mis-namespaced variants remain. `TheHuman/Health/ADHD` is now confirmed as the canonical Obsidian-side tag for the ADHD vocabulary row in step 2.

2. ✅ Done 2026-09-13—[[SoT - Canonical Interest Tags]] written: the Rosetta Stone mapping [[Reference - Vault Interest Map]]'s core interests to Obsidian tag/hub, Calibre Tag/Shelf, and Archilles keyword. Only the ADHD row is populated (per step 3, pilot-first); the other 11 are stubs with unconfirmed Calibre-side hints only, deliberately not decided yet. No Todoist column, per the 2026-09-13 scope decision.
3. Pilot on ADHD only before rolling out to the other 11 interest nodes—it's the dominant, most-structured cluster (its own MOC hub, ~90+ zettels, 10 Calibre tags), so it will surface every awkward edge case (naming mismatches, sub-topic granularity, whether BookFusion Shelf or Calibre Tag is the right anchor) while the blast radius of getting it wrong is contained to one node. Already surfacing an edge case before the pilot even starts: ADHD has no BookFusion Shelf of its own at all—ADHD books scatter across Mindfulness/Productivity/Family shelves depending on content—so for this node specifically, Calibre Tag (not Shelf) has to be the anchor, contradicting the general "Shelf=broad, Tag=fine" rule from Phase 2. And Obsidian's own ADHD tagging turns out to be just as messy as Calibre's was before this session's cleanup: bare `ADHD`, `adhd`, `ADHDers`, and sub-paths like `ADHD/productivity` all coexist in frontmatter, alongside the `TheHuman/Health/ADHD` namespaced form. The pilot will need a small Obsidian tag-cleanup pass of its own before the cross-tool mapping can be written down cleanly—this vault has the same problem Calibre had, just not yet fixed.
4. ~~Decide what "Things I want to learn" becomes~~—dropped, Todoist out of scope (2026-09-13).
5. ✅ Done and verified 2026-09-13—pilot Hookmark hooks for the ADHD hub. Corrected an earlier wrong assumption in this note: Hookmark wasn't "barely used"—it already held 192 real bookmarks, including 12 untagged ADHD-related Google Docs. Once properly installed as a real app (chezmoi/brew cask, Pro licence), its real AppleScript API (`hook.sdef`) was inspected directly, and the hub link was built and _verified_ for real: an Obsidian-MOC bookmark and a representative Calibre-book bookmark, hooked together, confirmed bidirectional via `hooked bookmarks`. All 14 ADHD-matching bookmarks (12 Google Docs + 2 new) were then tagged `ADHD` natively in Hookmark and `bookmarks with tags {"ADHD"}` confirmed to return all 14—a fourth real cross-tool layer (Google Docs + Obsidian + Calibre, one query) that wasn't in the original plan at all. See [[SoT - Canonical Interest Tags]] for full detail. One limitation remains genuinely unresolved: Calibre has no predictable tag-search URL (GUI-generated only via "Copy search as URL"), so the Calibre side still anchors on one representative book, not a live search over all 10 ADHD-tagged books.
6. Leave the filesystem out of scope for now—no evidence surfaced of loose files that need this treatment; revisit only if that turns out to be wrong.
7. Only after the ADHD pilot proves out, decide whether to extend to the other 11 core interests, and whether that extension should be manual (matches the vault's general preference for human curation) or scripted (a `calibredb` + Todoist-MCP + Obsidian pass, similar in spirit to this session's Calibre reconciliation work).

---

## 4. New Inputs from the PKM Meta-Graph Research (2026-09-13)

Atomized and promoted into `00_Inbox/` this session (13 notes, [[_link_report_pkm-meta-graph-system-research|link report]]). Three findings actually bear on this plan; the rest (Feynman's Twelve Favorite Problems, Sweller's cognitive load, the Collector's Fallacy, apophenia in graph views) are useful general PKM hygiene but don't change anything decided or open here.

- The Shelf/Tag tension in step 1 and step 3 has a name and a rule now. [[A Faceted PKM Schema Should Separate Domain (Visible Subject) from Theme (Cross-Cutting Mechanism)]] (extending [[Ranganathan's PMEST Facets Decompose a Subject Without Forcing a Single Parent Category]]) reframes "BookFusion Shelf vs. Calibre Tag" as a Domain vs. Theme split, not just two granularities of the same thing: Shelf already plays the Domain role (visible subject, one per book), Tag already plays something closer to Theme (a cross-cutting mechanism, many per book)—which is _why_ ADHD has no Shelf of its own (step 3's finding): ADHD is a Theme that cuts across Mindfulness/Productivity/Family Domains, not a Domain itself. The atom's proposed discipline—promote a term from Theme to Domain only once it demonstrably bridges 3+ existing Domains—is a concrete, testable rule for the still-open "is Shelf or Tag the right anchor" question below, and for [[SoT - Canonical Interest Tags]]'s eventual non-ADHD rows: don't invent new Shelves speculatively, promote a Tag to Shelf-equivalent status only once it's shown to bridge 3+ Domains in practice.
- A genuine vocabulary conflict, flagged rather than adopted. The research proposes its own 8-predicate edge vocabulary (is a/part of/supports/challenges/applies to/enables/derived from/contrasts with) for exactly this kind of cross-tool interest graph. [[A Proposed Eight-Predicate Edge Vocabulary for Typed PKM Links]] is typed `contradicts` against [[SoT - Typed Edge Vocabulary (Knowledge Graph Relations)]]—only `supports` overlaps; the other 7 fall outside the vault's closed set enforced by `edge_lint.py`. This plan does not need typed edges between tools (Hookmark's own hook/tag model already does the cross-tool linking job, per §2 above)—but if a future iteration ever wants to express _why_ two cross-tool items are linked (not just _that_ they are), this is the decision point: extend the vault's vocabulary deliberately, or keep cross-tool links untyped and leave typed edges to Obsidian-internal claim notes only.
- A candidate way to test the "ADHD is the dominant hub" assumption empirically. [[Betweenness Centrality Identifies Interdisciplinary Bridge Concepts]] links directly to this HEAD note. Right now "ADHD is the dominant hub" rests on [[Reference - Vault Interest Map]]'s manual LLM ranking (note count, MOC count). Betweenness centrality—how often a node sits on the shortest path between other node pairs—is a computable alternative: if the vault's typed-edge graph were run through a graph library, it would show which interest nodes actually _bridge_ the most other clusters, which may or may not be ADHD. Not worth doing before the ADHD pilot (step 3) finishes, but worth keeping as a way to sanity-check step 7's "which of the other 11 interests matters most" ordering rather than relying on manual ranking a second time.

---

## Open Questions

- Is BookFusion Shelf (broad, 21 values) or Calibre Tag (fine-grained, 62 values) the right anchor to mirror into Todoist labels and the vocabulary SoT—or both, at different granularities? Partially answered 2026-09-13: frame this as Domain (Shelf) vs. Theme (Tag) per §4 above, and apply the "3+ Domains bridged before promotion" rule rather than deciding per-node by feel.
- What are `pkm`, `hermes`, `1-Next_Action`, `2-Project`, `idea`, `needs-decision` (Todoist shared labels not in the personal label list) actually for, and do any of them already overlap with what this plan is trying to build?
- Is the Hookmark database's location on `/Volumes/DAL/Zettelkasten/Hookmark/` deliberate, and does it matter for this plan?
- Does regenerating [[Main Topics of Interest]] want to happen by hand, or is it worth scripting given it'll need to happen again every time the Calibre tag vocabulary changes?
- New 2026-09-13: if this plan ever needs to express _why_ two cross-tool items are linked, does it extend the vault's closed typed-edge vocabulary to cover cross-tool relations, or deliberately keep cross-tool links untyped (Hookmark tags/hooks only) and reserve typed edges for Obsidian-internal claim notes? See [[A Proposed Eight-Predicate Edge Vocabulary for Typed PKM Links]].

## Related

- [[Reference - Vault Interest Map]]—the existing ranked interest-node list this plan treats as canonical.
- [[Main Topics of Interest]]—the existing, now-stale Obsidian↔Calibre bridge artifact.
- [[MOC - ADHD (The Master Map)]]—the proposed pilot hub.
- [[SoT - Tool - NotebookLM]]—how NotebookLM is currently used.
- [[AGENTS.md]]—vault write-scope and typed-edge conventions this plan should stay consistent with if it ever touches claim notes.
- [[A Faceted PKM Schema Should Separate Domain (Visible Subject) from Theme (Cross-Cutting Mechanism)]]—the Domain/Theme framing and promotion rule behind §4.
- [[A Proposed Eight-Predicate Edge Vocabulary for Typed PKM Links]]—the vocabulary-conflict finding behind the new open question above.
- [[Betweenness Centrality Identifies Interdisciplinary Bridge Concepts]]—candidate method for empirically testing the "ADHD is the dominant hub" assumption.
- [[_link_report_pkm-meta-graph-system-research]]—full link report for the 2026-09-13 PKM Meta-Graph research atomization.
