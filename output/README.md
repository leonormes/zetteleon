---
title: Output Directory
created: 2026-05-10T00:00:00+00:00
modified: 2026-05-10T00:00:00+00:00
tags: [output, index, agent-protocol]
---

# Output — Synthesised Deliverables

This directory contains **final deliverables** generated from wiki/ knowledge. Outputs are synthesised from wiki pages only — never written directly from raw/ sources.

## Structure

| Subdirectory | Content Type | Example |
|--------------|--------------|---------|
| `reports/` | Full analytical reports | `2026-05-10-report-project-alpha.md` |
| `briefs/` | Executive summaries | `2026-05-11-brief-stakeholder-update.md` |
| `scripts/` | Generated scripts or code | `2026-05-12-script-data-pipeline.py` |
| `summaries/` | Condensed digests | `2026-05-13-summary-weekly-synthesis.md` |
| `plans/` | Implementation plans | `2026-05-14-plan-q2-roadmap.md` |

## Frontmatter Template

```yaml
---
title: <Document Title>
output_type: report | brief | script | summary | plan
created: <ISO 8601>
wiki_sources: [<list of wiki/ pages used>]
tags: [output, <type>]
---
```

## Naming Convention

```
output/YYYY-MM-DD-<type>-<slug>.md
```

Examples:
- `output/2026-05-10-report-nhs-integration.md`
- `output/2026-05-11-brief-executive-summary.md`
- `output/2026-05-12-plan-sprint-23.md`

## Agent Protocol

Outputs are **Layer 3** of the three-layer agent architecture:

| Layer | Path | Purpose |
|-------|------|---------|
| 1 | `raw/` | Immutable source material |
| 2 | `wiki/` | Agent-compiled knowledge |
| 3 | `output/` | Synthesised deliverables (this directory) |

**Golden Rule:** Outputs must cite wiki/ sources, which in turn cite raw/ sources. This creates a traceable knowledge chain.

## Related

- [[../wiki/index|Wiki Index]] — Source knowledge layer
- [[../AGENTS]] — Full agent protocol specification

---

*This directory is ready for use. Create your first output deliverable to establish the pattern.*
