---
created: 2026-06-29T07:45:39+00:00
modified: 2026-06-29T07:47:08+00:00
permalink: llmeon/00-inbox/pkm-agent-audit-prompt-for-claude
title: PKM Agent Audit — Prompt for Claude
type: note
---

## PKM Agent Audit—run This against My Config and Obsidian Vault

You are auditing how my LLM agents are configured to maintain my personal knowledge base (PKM), and the actual state of that PKM. I have had agents running against my vault for a while and am seeing no benefit. Your job is to find out why, then produce a lean improvement plan. You have filesystem access to my machine (macOS).

Do not modify any existing config or note. This is a read-only audit. The only file you create is the report. Stop before making any change and wait for my approval.

---

### Who I Am (so Your Plan is Targeted, not generic)

- Platform/DevOps engineer. ADHD: task-initiation is my constraint, so remedies must be single concrete physical actions, not "set up X".
- Goal of the PKM: extend cognition and force rigour—not passive archiving. I want commitments I can defend, not summaries.
- Known failure mode 1: I over-build—I add structure before consolidating. Your plan must remove/merge before it adds, and justify any new artefact.
- Known failure mode 2: I drift toward recognition over generation. An agent that does my thinking for me makes this worse.
- Output discipline: British English; no preamble; no sycophancy; depth over brevity with mechanisms explained.

### My Vault Ontology (use This to Judge conformance)

- Seven note types: Claim, Concept, Practice, Source, Person, Question, Literature (`Lit:`).
- Claim cards carry: a steel-manned sentence, explicit falsifiers, a named crux, a dated confidence position, open threads, counter-positions.
- Typed links only: `prerequisite_of`, `instance_of`, `contrasts_with`, `supports`, `related_to`.
- Three-layer granularity: Domain Hub → thesis-level Claims → support cards.
- YAML frontmatter fields include `type`, `tags`, `created`, `status`, `related_to`, `contrasts_with`.
- Question notes named `Q — [title].md`.
- Single Source of Truth (SoT): superseding a position requires `supersedes:` frontmatter plus a one-line diff narrative; the prior note is never deleted.

### Design Principle the Plan Must Enforce

The agent owns the source-digest layer; I own the claim layer. The agent may ingest sources, write `Source`/`Lit:` notes, maintain cross-links and indexes, and propose `Claim`/`Question` stubs for my review—but it must never author or edit a Claim card. Every factual statement an agent writes carries `[source]` (named citation) or `[inference]`; unattributed inference is a defect.

### My stack—discovery Targets (verify Actual Paths; These Are Starting Points, not assumptions)

- Hermes Agent (primary maintainer): locate its config / agent definition / system prompt; how it is triggered (`~/Library/LaunchAgents/`, launchd, cron, or manual); and its logs.
- mcp-proxy aggregator: its config and which MCP servers it exposes.
- Basic Memory: its config and projects—I intended a two-project split (curated Zettelkasten vs raw session capture); confirm where each project actually writes.
- Pieces MCP.
- Claude Desktop: `~/Library/Application Support/Claude/claude_desktop_config.json`.
- Claude Code: `~/.claude/`, any `CLAUDE.md`, `settings.json`.
- Any `AGENTS.md` / system-prompt files in or near the vault.
- chezmoi source: `~/.local/share/chezmoi` (my dotfiles are managed here—a live config may be a generated copy of a source under chezmoi).
- The vault: on an external volume—locate the path; inspect `.obsidian/` for plugins (Dataview, Bases); determine whether it is a git repo.

---

### Rules (non-negotiable)

1. Read-only on everything that already exists. Create only the report.
2. Evidence or it didn't happen. Tag every finding `[source]` (give the `path` and line/snippet you actually read) or `[inference]`. If something isn't found, write "not found at: \<locations searched>"—never assume it exists or doesn't.
3. Quantify wherever possible: conformance %, counts of orphans/duplicates/broken links, days since last agent write, run cadence.
4. chezmoi-aware: for each config, check whether it is chezmoi-managed and report both the live path and the source path. Any edit recommendation targets the source, not the generated copy.
5. Distinguish agent-written from hand-written notes—this is the linchpin. Establish a reliable signal early (a frontmatter `source`/author field, git commit author, a tag, or a path convention) and state which signal you used.
6. Lean remedy. Remove and consolidate before adding. Default to fewer agents, fewer configs, fewer instructions.
7. British English. No preamble.

### Phase 1—Inventory the Agents and Config (breadth first)

Find every config governing an agent that can read or write the vault. Produce an inventory table:

| Agent | Config path(s) | chezmoi-managed? | Trigger & cadence | Declared job | Writes to (path) | Last activity (evidence) |

### Phase 2—Reconstruct Intended Behaviour

For each agent: what is it _instructed_ to do to the vault (verbatim where possible)? What triggers it and how often? Where is its output meant to land? Then flag overlaps, conflicts, and gaps between agents, and state whether a single source of truth for agent behaviour exists or whether instructions are duplicated and divergent.

### Phase 3—Audit the Actual Vault State (evidence-driven; Don't Read everything)

- If it's a git repo: `git log` for agent-attributable commits—cadence, last agent commit, volume.
- Timestamps: most-recently-modified notes; split agent-written vs hand-written using your Phase-0 signal.
- Are there any agent-generated notes? Do they sit in the curated vault, or in a capture sink that never gets promoted?
- Conformance sample: take (a) the 15 most-recently-modified notes, (b) a random 15, (c) all agent-written notes you can find. For each, check against the ontology—correct `type`? valid typed links? do Claim cards have steel-man / falsifiers / crux? are `[source]`/`[inference]` tags present? Report a conformance rate.
- Drift markers: near-duplicates (SoT violations), orphans (no inbound links), broken links, stale claims, notes with no `type`, capture-sink bloat.

### Phase 4—Diagnose the Gap

Map intended (Phase 2) against actual (Phase 3) and identify which failure mode(s) explain "no benefit", each backed by evidence:

- (a) Not running—trigger broken or erroring silently. Cite last run and logs.
- (b) Running into a sink—writing to raw-capture, never promoted to the curated vault.
- (c) Non-conforming—writing, but output doesn't match the ontology, so it never integrates.
- (d) Never surfaced—conforming, but nothing brings it into my workflow, so benefit is invisible.
- (e) Config sprawl / conflict—multiple agents with overlapping or divergent instructions.
- (f) Too generic—instructions produce summaries, not commitments (violates the source-digest/claim boundary).

State the dominant cause and any contributors, in one evidence-tagged paragraph.

### Phase 5—Improvement Plan

- Consolidate config: name the single canonical agent-behaviour spec to keep; list every other config to retire, merge, or point at it. Route edits through chezmoi.
- Correct drift: the specific, ordered clean-up actions (dedupe, fix links, retype, promote-or-archive the sink), each tied to a Phase-3 finding.
- Make it useful: the smallest changes that produce _visible_ benefit—enforce the source-digest/claim boundary in the canonical spec, and add one surfacing mechanism so output enters my workflow (e.g. a Dataview/Bases query listing agent-proposed Claim/Question stubs awaiting my review).

Constraints on the plan: remove before adding; every step is one concrete physical action; prioritised (do-first → later); flag anything that risks the vault.

### Output

Write the audit as a single markdown file in my obsidian vault /Volumes/DAL/Zettelkasten/LLMeon/00_Inbox/ Sections: Inventory · Intended-vs-actual · Vault state · Diagnosis · Improvement plan. End with the single next physical action. Then stop and wait for my approval before changing anything.
