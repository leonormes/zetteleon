---
created: 2026-07-11T00:00:00+00:00
permalink: llmeon/output/reports/vault-pattern-audit
tags: [report, pkm, audit]
title: Vault Pattern Audit — 2026-07-11
---

## Vault Pattern Audit

Full-vault scan, 2026-07-11. 2,332 markdown notes analysed (excluding `.trash`, which holds another 1,202). Method: complete filesystem + git-history analysis of every note, link, tag, and frontmatter field.

---

### Headline

**You do have a system. You have five.** The mess is not an absence of structure — it is *stratigraphy*: successive systems layered on top of each other, each partially migrated into the next. The current one (ProdOS, April 2026) is the best-designed and, unusually, it is actually running. The problem to solve is not "build a system" but "finish demolishing the previous four".

---

### Pattern 1 — The archaeological strata

Five generations of PKM are visible in the vault, oldest to newest:

1. **Heptabase era** — 238 notes sitting in `.trash/Heptabase/` (imported card library, never integrated).
2. **Luhmann-ID Zettelkasten** — folgezettel-style names still live in `100_zettelkasten/`: `7-cybernetics.md`, `2c. Propositions...`, `5c-emergence.md`, `21-wtf_is_knowledge_anyway.md`. More in trash (`1a1-complex_from_simple`, `14a-appeal_to_authority`).
3. **Johnny-Decimal / PARA hybrid** — the numbered top folders (`00_Inbox`, `01_journals`, `10_System`, `20_Thinking`, `30_Library`, `99_Archive`) plus nested numbering inside `30_Library` (`100_`, `200_`, `400_`).
4. **GTD overlay** — 63 files reference GTD; Todoist integration; "Next Action" atoms; GTD-context prompts in `10_System/prompts/`.
5. **ProdOS (current)** — created 2026-04-28: `AGENTS.md` rulebook, three-layer agent memory (`raw/` → `wiki/` → `output/`), Hermes-maintained `index.md` and append-only `log.md`, SoT/Protocol/HEAD/MoC note types.

Each migration was ~80% completed. The remaining 20% of each is what reads as "mess".

### Pattern 2 — The February 2026 inflection (this is the good news)

Daily notes tell a clear story:

- **Feb 2025 → Jan 2026**: ~71 daily notes in ~11 months. Sporadic — bursts of 3–5 days, then multi-week gaps. Classic novelty-decay curve.
- **8 Feb 2026 → today**: near-perfect streak. Roughly **150 of 154 days** (missed only ~12 Feb, ~13 May, 6–7 Jun, 1 Jul).

Something changed in February and it *stuck* — pre-dating ProdOS by two months. Whatever the February change was (the streak itself, the LLM-as-Chief-of-Staff workflow, or both), it is the single most successful behavioural intervention in the vault's history. Worth identifying and protecting.

Also working: `00_Inbox` contains **2 files** (not two hundred), `index.md` is auto-maintained, `log.md` shows continuous agent ingestion since April, and `raw/` has 140 consistently named capture files. The automated layer is not the mess.

### Pattern 3 — The recursion trap

**232 of 1,074 zettelkasten notes (~22%) are about productivity, ADHD, PKM, or note-taking itself.** Sixty-three files mention GTD; there are MoCs titled "MOC - ADHD Project Continuation Challenge" and "MOC - ADHD Hyperfixation-Burnout Cycle" — the vault contains an accurate diagnosis of its own failure mode.

This is the knowing-doing gap made visible: the system is the novelty, so building the system is what gets the dopamine. The theory layer is world-class; it is also a fifth of the vault.

### Pattern 4 — Projects have six homes

Project-ish material currently lives in **six competing locations**:

| Location | Contents |
|---|---|
| `wiki/projects/` | Agent-maintained work projects (the healthy one) |
| `30_Library/200_Projects/` | Work docs + Bessie's GCSE plans + `Art.md`, mixed numbering schemes |
| `jira/` | 10 ticket notes |
| `Work/` + `Work/Jira/` | 5 more work notes, overlapping the same FTFL tickets |
| Root ad-hoc folders | `AWS/`, `Claims/`, `Practices/`, `security/`, `research/` (research/ contains 0 notes) |
| `.trash/Projects/`, `.trash/200_projects/` | previous attempts |

`jira/FTFL-511...` and `wiki/projects/FTFL-511 Nginx HTTPS Hardening` describe the same ticket. Every capture decision currently requires answering "which of six folders?" — that is activation-energy tax on every single note.

### Pattern 5 — Schema drift in frontmatter

`AGENTS.md` declares `prodos.kind`/`prodos.lifecycle` canonical and bans legacy keys. Reality:

- Legacy `type:` — **1,924 notes**, with 12+ inconsistent values including `''`, `null`, `'null'`
- New `prodos.kind:` — **~110 notes**
- `status:` 1,625, `updated:` 1,406, `last_reviewed:` 1,295 — all officially deprecated, all dominant

The migration is 5% done. Any Dataview/Bases query written against the new schema silently misses 95% of the vault.

### Pattern 6 — Linking health is mid-migration too

Of 1,074 zettelkasten notes: **391 (36%) link out to nothing**, 197 (18%) have nothing linking in, and 88 are full orphans. Vault-wide, **543 notes (23%) are complete islands**. Counterweight: 108 MoCs exist and the `_link_report_*` files in `400_indexes` show an agent workflow already built for exactly this repair job — it just hasn't been run to completion.

Note quality itself is fine: median atomic note is ~1,200 characters — properly atomic, not stubs.

### Pattern 7 — Naming conventions (four in one folder)

`100_zettelkasten/` alone mixes: Luhmann IDs (`7-cybernetics`), letter-decimal (`2c.`), full-sentence claim titles (the majority, and the current standard), and `Claim -` / `Q —` prefixes. `200_Projects` adds decimal numbering (`1.3`, `2.1` for GCSE subjects), date-prefixed files, and one filename that is a truncated paragraph ("Based on the Ofsted report, the UK government's implied expectations…com.md").

---

## What this means

The ADHD pattern here is not abandonment — it's **serial 80% migrations**. Each new system was genuinely better than the last, each got most of the content moved, and each left a residue that makes the whole feel chaotic even though the *current* system (ProdOS + Hermes + daily streak) is functioning well.

The principle: **entropy in this vault comes from ambiguity, not volume.** Six project homes and two frontmatter schemas mean every note faces a fork in the road; forks are where executive function stalls. Every fix below removes a fork rather than adding structure.

### Recommendations (in order, each independently valuable)

1. **Do not adopt a sixth system.** ProdOS is working. Declare it final by writing one line in `AGENTS.md`: "Folder taxonomy is frozen as of 2026-07-11."
2. **Collapse the six project homes to two**: `wiki/projects/` (agent territory) and `30_Library/200_Projects/` (human territory). `jira/`, `Work/`, `AWS/`, `Claims/`, `Practices/`, `security/`, `research/` merge in or go to `99_Archive/`. Family/GCSE material gets its own subfolder so it stops cohabiting with Terraform docs.
3. **Automate the frontmatter migration** — this is a script's job, not willpower's. One agent pass: map legacy `type:` values → `prodos.kind`, delete `status`/`updated`/`last_reviewed`. 1,924 notes, one afternoon of compute, zero human decisions after the mapping table is agreed.
4. **Run orphan triage as an agent cron**, like the existing `_link_report_` workflow: 10 orphans per day proposed for linking or archiving. 88 zettelkasten orphans = done in 9 days without you touching it.
5. **Empty `.trash` for real** (1,202 notes, including all of Heptabase). It's in git history if ever needed. A 34% reduction in vault mass for one command.
6. **Ration meta-productivity notes.** The 22% recursion is the hyperfixation channel. A practical valve: new PKM-about-PKM atoms require an inbound link from a *non*-meta note within a week, or they route to `99_Archive`.

### The immediate next physical action

Open a terminal and run:

```
mv jira Work/Jira-old && ls Work
```

Two folders become one. Thirty seconds. Everything else above can be delegated to Hermes as `/goal` prompts — items 3 and 4 are precisely the kind of bounded, mechanical work the agent layer already does well.

---

*Method note: the Obsidian MCP connection exposed file-access tools but no semantic-search endpoint, so this audit used full-corpus scanning (every note read and parsed) — broader coverage than sampled semantic search. Figures verified against a second counting pass.*
