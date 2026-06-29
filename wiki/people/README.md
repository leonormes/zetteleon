---
title: People Index
created: 2026-05-10 00:00:00+00:00
modified: 2026-05-10 00:00:00+00:00
tags:
- wiki
- people
- index
permalink: llmeon/wiki/people/readme
---

# People — Individual Entity Dossiers

This subdirectory contains **people dossiers** — structured knowledge about individuals extracted from raw/ sources.

## When to Create a People Dossier

Create a people dossier when you encounter:
- A **colleague** or stakeholder mentioned in meetings
- A **researcher** or author cited in source material
- A **contact** or professional relationship
- A **public figure** relevant to your work

## Frontmatter Template

```yaml
---
title: <Person Name>
wiki_type: dossier
entity_kind: person
created: <ISO 8601>
modified: <ISO 8601>
tags: [wiki, dossier, person]
sources: [<list of raw/ filenames that support this page>]
---
```

## Mandatory Sections

### Summary
One-paragraph overview of the person.

### Key Facts
Bulleted claims, **each with an inline citation**:
```markdown
> "verbatim quote or fact" — [[raw/YYYY-MM-DD-source-slug]]
```

### Connections
`[[Wikilinks]]` to related people, organisations, projects, and concepts.

### Timeline
Dated milestones sourced from raw notes (e.g., meetings, collaborations, role changes).

### Contradictions
Any claims that conflict across sources (flag, do not resolve).

### Open Questions
Gaps that cannot be filled from existing raw material.

## Examples

*No people dossiers yet — create the first one to establish the pattern.*

## Related

- [[../orgs/|Organisation dossiers]] — Companies, institutions
- [[../concepts/|Concept pages]] — Frameworks and domain knowledge
- [[../projects/|Project dossiers]] — Active and archived projects

---

*This directory is currently empty. The first people dossier should be created from existing raw/ sources or new ingested material.*