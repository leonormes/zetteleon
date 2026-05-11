---
title: Concepts Index
created: 2026-05-10T00:00:00+00:00
modified: 2026-05-10T00:00:00+00:00
tags: [wiki, concepts, index]
---

# Concepts — Frameworks, Ideas, and Domain Knowledge

This subdirectory contains **concept pages** — structured knowledge about ideas, frameworks, processes, and domain expertise extracted from raw/ sources.

## When to Create a Concept Page

Create a concept page when you encounter:
- A **framework** or methodology (e.g., "Morita Therapy", "Getting Things Done")
- A **domain concept** (e.g., "Access Control Lists", "Emotional Reasoning")
- A **process** or workflow (e.g., "Research-to-Action Protocol")
- A **theoretical model** (e.g., "Action Dominance", "ADHD Brain Wiring")

## Frontmatter Template

```yaml
---
title: <Concept Name>
wiki_type: concept
entity_kind: concept
created: <ISO 8601>
modified: <ISO 8601>
tags: [wiki, concept]
sources: [<list of raw/ filenames that support this page>]
---
```

## Mandatory Sections

### Summary
One-paragraph overview of the concept.

### Key Facts
Bulleted claims, **each with an inline citation**:
```markdown
> "verbatim quote or fact" — [[raw/YYYY-MM-DD-source-slug]]
```

### Connections
`[[Wikilinks]]` to related concept pages and dossiers.

### Contradictions
Any claims that conflict across sources (flag, do not resolve).

### Open Questions
Gaps that cannot be filled from existing raw material.

## Examples

*No concept pages yet — create the first one to establish the pattern.*

## Related

- [[../people/|People dossiers]] — Individual entities
- [[../orgs/|Organisation dossiers]] — Companies, institutions
- [[../projects/|Project dossiers]] — Active and archived projects
- [[../../30_Library/100_zettelkasten/|30_Library/100_zettelkasten/]] — Atomic notes (human-authored)

---

*This directory is currently empty. The first concept page should be created from existing raw/ sources or new ingested material.*
