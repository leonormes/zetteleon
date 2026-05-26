---
created: 2026-04-14T20:17:56+00:00
created_utc: "2026-04-14T12:40:00Z"
kind: mechanism
modified: 2026-05-26T11:44:36+00:00
source_title: "CUE — A Type System for the Cloud"
source_url: "https://www.youtube.com/watch?v=FsUytTpDNro"
status: seed
tags: [cue, policy-enforcement, Profile, schema-validation, strictness]
title: Closed Type Definitions
type: atom
upstream: "[[SoT - CUE Configuration]]"
---

## Closed Type Definitions

Closed definitions in CUE (using the `#` symbol) prevent the addition of fields that are not explicitly defined in the schema. This mechanism ensures strict policy enforcement by flagging any "shadow" or unrecognised configuration fields as errors during evaluation.

### Scope & Conditions

Essential for strict architectural enforcement and robust schema validation in large configurations.

### Evidence

> "By using the # symbol (e.g., Profile), you can create 'closed' definitions. This prevents accidental addition of fields that aren't explicitly defined in the schema."

### Implications

- Prevents typographical errors from becoming valid but unintended new configuration values.
- Vital for maintaining the integrity of large-scale configurations by ensuring only allowed properties are present.

### Related

- [[SoT - CUE Configuration]]—direct concept match: closed definitions as a tool for robust composition.
- [[Pattern - Helm Chart as a Compiler]]—shared mechanism: uses closed definitions to ensure the "Compiler" only receives valid "Intent."

### See Also

- [[Configuration Unification]]
