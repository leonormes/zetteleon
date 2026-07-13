---
created: 2026-07-11 14:25:29+00:00
modified: 2026-07-11 14:59:47+00:00
title: LLMeon_Vault_Pattern_Report
project_name: ProdOS
permalink: llmeon/00-inbox/llmeon-vault-pattern-report
---

## LLMeon Vault Pattern Report

Scope: Direct structural/statistical analysis of `/Volumes/DAL/Zettelkasten/LLMeon` (2,335 active notes + 1,202 in `.trash`, git history back to Nov 2025, daily notes back to Feb 2025).

A note on method: I don't have your "obsidian 1mcp" semantic-search server available as a connector in this environment, so I didn't run embedding-based clustering. Instead I read the vault directly—folder structure, git history, frontmatter, links, tasks—across all 2,335 notes. This actually surfaces something semantic search would miss: when and how each part of the system was built and abandoned. If you want the semantic layer too, your local MCP setup (Claude/Warp) can complement this with topic clustering on top of what's below.

---

### The One Pattern behind All the Others

You're not failing to find a system. You've built at least four complete, well-designed systems (numbered PARA vault, Zettelkasten with progressive-summarization statuses, GTD-style CRPE loop, and a full agentic "ProdOS" with an AI Chief of Staff). Each one is architecturally sound. None of them died from a bad idea—they died because designing the system is the engaging part, and using it day-to-day isn't. The evidence for this is everywhere in the data below: new top-level folders appear every 2–3 weeks, 20+ bespoke AI prompts exist to _fix the vault_ rather than notes that _use_ it, and your most sophisticated system (ProdOS) has unresolved setup questions sitting untouched for over five weeks.

---

### Quantitative Snapshot

| Metric | Value |
|---|---|
| Active notes | 2,335 (100% have frontmatter) |
| Notes in `.trash` (never purged) | 1,202 |
| Unique frontmatter schemas in use | 209 |
| Distinct `status` values | 38 (incl. literal strings `'null'` and `''`) |
| Distinct `type` values | 70+ (incl. typos like `projec`, malformed `wiki_type: dossier`) |
| Total wikilinks | 6,549 |
| Notes with zero outgoing links | 1,128 (48%) |
| Wikilinks pointing to notes that don't exist | ~1,330 (~20%) |
| Open `- []` tasks embedded in notes | 583 (across only 69 files) |
| Completed `- [x]` tasks in notes | 160 |
| New unmerged top-level folders since Dec 2025 | 12 |

---

### Pattern 1—A New Folder Appears Every 2–3 Weeks, None Get Merged back

Your core structure (`00_Inbox`, `01_journals`, `10_System`, `20_Thinking`, `30_Library`, `99_Archive`) was created 9–20 December 2025. It's a solid numbered system. But since then, a new, ungoverned top-level folder has appeared roughly every 2–3 weeks and never been absorbed into it:

| Folder | First appeared | Files now |
|---|---|---|
| `wiki/`, `raw/` | 29 Apr 2026 | 82 / 140 |
| `security/`, `output/`, `research/` | 11 May 2026 | 2 / 2 / 0 |
| `Work/` | 2 May 2026 | 5 |
| `jira/` | 28 May 2026 | 10 |
| `Templates/` | 16 Jun 2026 | 2 |
| `AWS/` | 29 Jun 2026 | 2 |
| `Practices/`, `Claims/` | 7 Jul 2026 (4 days ago) | 1 / 1 |

Each one starts with real intent, gets 1–10 files, then stalls. `Templates/` (2 files) sits alongside `10_System/templates/` (6 files)—a second, competing templates folder. This is the clearest fingerprint of novelty-driven restructuring: it's easier to start a new container than to decide where something already goes.

### Pattern 2—You Keep Building the AI that Will Fix the Vault, instead of Fixing the Vault

`10_System/prompts/` contains 20 different bespoke prompts, most of them written _for an AI agent to organize this exact vault_: Principal Vault Triage Architect, Knowledge Consolidation Agent, Knowledge Harvesting & Normalization Agent, Note Refresh & Link Auditor, Atomic Linker → Promote & Connect, Atomic Signal Extractor, sys_merger, ProdOS Chronos Synthesizer, ProdOS MoC Cartographer, ProdOS Protocol Architect, plus six `leon-context-*` personal-context files for feeding your profile to LLMs.

This is meta-work masquerading as the task. Writing a prompt that describes how a triage system _should_ work is intellectually satisfying and gives immediate feedback (a good ADHD reward loop)—but it substitutes for actually triaging. It's the same reason this exact conversation ("review my vault with a tool") is comfortable ground.

### Pattern 3—A Taxonomy Was Designed, then Nobody Enforced it

You clearly designed a real Zettelkasten status model (`seedling → seed → stable/evergreen`, i.e. progressive summarization) and a `type` field for note kinds. But because nothing validates frontmatter on save:

- `status` has 38 distinct values, including the literal text `'null'` (130 notes) and empty string `''` (282 notes)—412 notes, ~18% of the vault, have no real status at all.
- `type` has 70+ distinct values. Most are used once or twice (`sn`, `projec`, `wiki_type: dossier`, `secret`, `tutorial`). No controlled vocabulary is being applied.
- 209 unique frontmatter key-combinations exist across 2,335 notes—meaning almost every batch of notes was created under a slightly different mental model of "what a note needs," usually because it was created via a different AI prompt or template version.

The system has good bones (Bricks/Architecture, epistemic confidence tracking—see your own `leon-context-pkm-philosophy.md`) but no enforcement layer, so entropy wins by default.

### Pattern 4—Half the Zettelkasten Isn't Actually a Zettelkasten

The point of atomic notes is that they connect. 1,128 of 2,335 notes (48%) have zero outgoing links—they're islands, indistinguishable from a folder of disconnected clippings. On top of that, roughly 1,330 wikilink references (~20% of all links) point to notes that don't exist—concepts referenced but never created, or renamed without updating backlinks. The zettelkasten folder (`30_Library/100_zettelkasten`, 1,074 notes—the single largest chunk of the vault) is where this matters most: without links, it's a pile, not a network.

### Pattern 5—Tasks Leak into Notes instead of Going to Todoist

Your own documented workflow says: _"Action? → Todoist."_ In practice, 583 open checkboxes exist inside 69 markdown notes, vs. 160 completed. Tasks are being captured in the moment (good—low friction) but not routed out to the system designed to hold them, so they pile up invisibly inside notes nobody re-opens.

### Pattern 6—Automation Gets Built, Spikes, and Dies within Weeks

The `raw/` folder (your automated "Daily Synthesis" capture pipeline from Pieces LTM) is a clean natural experiment:

| Month | Files created |
|---|---|
| Apr 2026 | 9 (pipeline just built) |
| May 2026 | 100 (peak usage) |
| Jun 2026 | 30 (declining) |
| Jul 2026 | 1 (effectively dead) |

Same story with `.context-engine-backups/`—a custom backup mechanism you built, used exactly once (13 Dec 2025), never again. And the `wiki/` entity system (people/orgs/projects/concepts/infrastructure—meant to build a linked knowledge graph of your work) is wildly lopsided: `wiki/projects` has 65 pages, while `people`, `orgs`, and `infrastructure` each have exactly 1. You built the scaffolding for all five, then only ever populated the one that was easiest (or most fun) to fill in.

### Pattern 7—The Documented System and the Real System Have Already Diverged

- `How to Use the prodOS Workflow.md` instructs you to capture everything into `00_Inbox/dump.md`. That file does not exist anywhere in the vault—the documented entry point to your own system was never created.
- `20_Thinking/21_Workbench` has an explicit rule: _"NO STORAGE—if not actionable in 24h, delete."_ Its actual contents include `HEAD` notes dated weeks apart (11 Jun, 16 Jun, 24 Jun, 29 Jun, 1 Jul) still sitting there, plus genuinely long-lived personal interests ("A Conceptual Map for Learning Mathematics," "Archery Practice," "The Neural Drivers of the Social Brain") that were never 24-hour thoughts to begin with—they're being mis-filed into a scratchpad because there's no better home.
- The ProdOS design doc itself ends with an "Open Questions—Not Yet Resolved" section (has the Hermes `/goal` prompt actually run? does the Teams MCP connector exist? is the Todoist token configured?) written 26 May and still unresolved as of the doc's last edit, 4 July—39 days later.

---

### What's Actually Working (Don't touch tHis)

- Daily notes stuck. Feb 2025–Jan 2026 they were sporadic (2–13/month). From Feb 2026 onward they jumped to 22–31 per month—essentially a daily habit, sustained for 5+ months through July 2026. This is your one genuinely durable system, and it's the lowest-friction one you have. It's proof you _can_ sustain a habit when it doesn't require deciding where anything goes.
- Frontmatter discipline is universal—literally 100% of notes have it, even if the schema drifts. The capture habit is fine; it's the categorization layer that's overbuilt.
- `10_System/prompts/` is genuinely reusable IP, not waste—it's just currently pointed at "redesign the system" instead of "run the system."

---

### Root Cause, in One Sentence

Every layer of this vault shows the same shape: high-effort architecture, low-effort maintenance, and a reflex to replace rather than repair—which is a completely predictable outcome of ADHD's novelty-reward bias meeting a domain (PKM) that rewards infinite meta-tinkering with genuine intellectual pleasure. The fix isn't a better system. You've already designed several good ones. The fix is treating "adding structure" as the thing to resist, not the thing to reach for.

---

### Concrete next Actions (Small, not aNother rEbuild)

1. Freeze new top-level folders for 30 days. Anything that doesn't fit `00–99` goes into `00_Inbox` until reviewed weekly, full stop. No new folder, no new template.
2. Kill the meta-tool backlog. Don't write another triage/consolidation agent prompt until the 20 you already have have each been run at least once against a real batch of notes.
3. Merge the orphans, not-relink them individually. Run a script against `30_Library/100_zettelkasten` to list the 1,128 zero-link notes; batch-review just the ones under 200 characters for deletion, and only manually link the ones worth keeping. Don't try to fix all 1,128—that's a new rebuild in disguise.
4. Pick one status vocabulary and regex-replace the rest. Collapse `'null'`, `''`, and missing status to one canonical `seed`, and stop there—don't redesign the taxonomy while doing it.
5. Stop letting tasks live in notes. Any `- []` outside Todoist gets swept into Todoist in one pass, then the rule "notes never hold open tasks" gets enforced going forward (a simple pre-commit or Obsidian linter can flag new `- []` outside a whitelist folder).
6. Empty `.trash` on a schedule. 1,202 trashed notes sitting forever isn't deletion, it's hiding—pick a purge cadence (e.g. monthly) so "delete" means delete, matching your own stated anti-hoarding goal.
7. Answer the three open ProdOS questions this week, or explicitly shelve ProdOS. A system with unresolved setup questions for 39+ days isn't paused, it's dead—better to know which.

If you want, I can turn any one of these into an actual script (e.g. a Python pass that finds and lists the 1,128 orphan notes, or one that normalizes the `status` field vault-wide) rather than another prompt describing how it should work.