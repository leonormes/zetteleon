---
created: 2026-04-14T20:26:31+00:00
created_utc: '2026-04-14T13:20:00Z'
kind: heuristic
modified: 2026-07-14T13:02:18+00:00
permalink: llmeon/30-library/100-zettelkasten/in-housing-dependencies
source_title: Archon and Extreme Harness Engineering
source_url: https://youtube.com/watch?v=qMnClynCAmM
status: seed
tags: [dependency-management, efficiency, technical-debt]
title: In-Housing Dependencies
type: atom
upstream: '[[SoT - Agentic AI Design Patterns]]'
---

## In-Housing Dependencies

As the cost of code generation becomes negligible, engineering teams should replace complex, generic external dependencies with minimal, specific logic generated locally by AI agents. This strategy reduces technical bloat and simplifies the codebase by including only the functionality required for the specific project.

### Scope & Conditions

Economically viable in environments where high-fidelity agentic generation is integrated into the workflow.

### Evidence

> "Because code generation is essentially free, teams can 'in-house' and strip down complex dependencies into a few thousand lines of specific, relevant logic."

### Implications

- Results in a smaller codebase surface area, which improves security and reduces maintenance overhead.
- Removes "just-in-case" functionality often found in general-purpose libraries, leading to more focused and understandable code.

### Related

- [[Software Complexity is Conserved Between Control Flow and Representation]]—shared mechanism: by in-housing, complexity is simplified and made more visible.
- [[SoT - Simple Made Easy (Rich Hickey)]]—supports: advocating for the removal of unneeded generic complexity.

### See Also

- [[Software as Specification (Ghost Libraries)]]
