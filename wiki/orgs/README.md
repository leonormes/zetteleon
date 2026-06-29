---
title: Organisations Index
created: 2026-05-10 00:00:00+00:00
modified: 2026-05-10 00:00:00+00:00
tags:
- wiki
- orgs
- index
permalink: llmeon/wiki/orgs/readme
---

# Organisations — Companies, Institutions, and Groups

This subdirectory contains **organisation dossiers** — structured knowledge about companies, institutions, government bodies, and other collective entities extracted from raw/ sources.

## When to Create an Organisation Dossier

Create an org dossier when you encounter:
- A **company** or employer (e.g., "NHS", "Microsoft", "OpenAI")
- A **government body** (e.g., "CQC", "NICE", "Department of Health")
- An **institution** (e.g., "University of Oxford", "BMJ")
- A **research group** or consortium

## Frontmatter Template

```yaml
---
title: <Organisation Name>
wiki_type: dossier
entity_kind: org
created: <ISO 8601>
modified: <ISO 8601>
tags: [wiki, dossier, org]
sources: [<list of raw/ filenames that support this page>]
---
```

## Mandatory Sections

### Summary
One-paragraph overview of the organisation.

### Key Facts
Bulleted claims, **each with an inline citation**:
```markdown
> "verbatim quote or fact" — [[raw/YYYY-MM-DD-source-slug]]
```

### Connections
`[[Wikilinks]]` to related people, projects, and concepts.

### Timeline
Dated milestones sourced from raw notes (e.g., contracts, partnerships, key events).

### Contradictions
Any claims that conflict across sources (flag, do not resolve).

### Open Questions
Gaps that cannot be filled from existing raw material.

## Examples

*No organisation dossiers yet — create the first one to establish the pattern.*

## Related

- [[../people/|People dossiers]] — Individual entities
- [[../concepts/|Concept pages]] — Frameworks and domain knowledge
- [[../projects/|Project dossiers]] — Active and archived projects

---

*This directory is currently empty. The first org dossier should be created from existing raw/ sources or new ingested material.*