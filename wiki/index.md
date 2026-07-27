---
title: Wiki Index
created: 2026-05-10 00:00:00+00:00
modified: 2026-07-25 19:02:23+01:00
tags:
- wiki
- index
- agent-protocol
permalink: llmeon/wiki/index
---

# Wiki Index — Agent Knowledge Layer

This is the entry point for the **agent-managed knowledge layer** of the LLMeon vault.

## Purpose

The wiki/ directory contains **agent-compiled knowledge** extracted from immutable source material in `raw/`. All claims in wiki pages must trace back to raw/ sources via inline citations.

## Structure

| Subdirectory | Content Type | Status |
|--------------|--------------|--------|
| [[wiki/concepts/|concepts/]] | Frameworks, ideas, processes, domain knowledge | ✅ Active (2 files) |
| [[wiki/orgs/|orgs/]] | Organisations, companies, institutions | 🟡 Empty |
| [[wiki/people/|people/]] | Individuals, contacts, stakeholders | 🟡 Empty |
| [[wiki/projects/|projects/]] | Project dossiers with timelines and milestones | ✅ Active (13 files) |

## Usage

### Creating a New Wiki Page

1. **Identify the entity type** → choose the correct subdirectory
2. **Extract facts from raw/ sources** → each fact needs a citation
3. **Use the template** → see subdirectory READMEs for frontmatter and structure
4. **Link to related pages** → use `[[Wikilinks]]` to connect knowledge
5. **Log the change** → add an entry to [[wiki/log]]

### Citation Format

Every claim in `## Key Facts` must include a raw/ backlink:

```markdown
> "verbatim quote or paraphrased fact" — [[raw/YYYY-MM-DD-source-slug]]
```

If sourced from Pieces LTM, include the Pieces ID:

```markdown
> "verbatim excerpt" — [[raw/YYYY-MM-DD-pieces-slug]] (Pieces: <pieces_id>)
```

## Agent Protocol

This wiki layer is **Layer 2** of the three-layer agent architecture:

| Layer | Path | Purpose |
|-------|------|---------|
| 1 | `raw/` | Immutable source material (append-only) |
| 2 | `wiki/` | Agent-compiled knowledge (this directory) |
| 3 | `output/` | Synthesised deliverables (reports, briefs, scripts) |

**Golden Rules:**
- Never edit a `raw/` file after creation
- Every wiki claim needs a `raw/` citation
- Contradictions must be surfaced, not resolved
- Log all changes in [[wiki/log]]

## Related

- [[AGENTS]] — Full agent protocol specification
- [[wiki/log]] — Change tracking and audit trail
- [[../30_Library/100_zettelkasten/|30_Library/100_zettelkasten/]] — Human-authored atomic notes
- [[../30_Library/200_projects/|30_Library/200_projects/]] — Human-authored project documentation

---

*Last updated: 2026-07-25*
