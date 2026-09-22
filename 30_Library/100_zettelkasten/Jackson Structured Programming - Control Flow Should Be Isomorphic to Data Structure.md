---
conformant: true
contradicts: []
created: 2026-09-19T15:25:22+00:00
created_utc: 2026-09-19 00:00:00+00:00
epistemic_status: medium
evidence_links: []
modified: 2026-09-22T00:00:00+00:00
non_conformance_reason: ''
permalink: llmeon/00-inbox/jackson-structured-programming-control-flow-should-be-isomorphic-to-data-structure
proposition: The 1975 Jackson Structured Programming method, created by Michael Jackson, derives a program control structure directly and exclusively from Data Structure Diagrams of its input and output, so sequences, iterations, and selections in the data are mirrored one-for-one by sequential blocks, loops, and conditionals in the code.
source_title: "The Conservation of Software Complexity: The Dichotomy of Data Structures and Control Flow (plus epistemic review/fact-check)"
source_url: unknown
status: seed
tags: [control-flow, data-structures, historical, jackson-structured-programming]
title: "Jackson Structured Programming - Control Flow Should Be Isomorphic to Data Structure"
type: claim
upstream: '[[tmp_atoms_data-structures-vs-control-flow]]'
---

## Jackson Structured Programming - Control Flow Should Be Isomorphic to Data Structure

Michael Jackson's 1975 Jackson Structured Programming (JSP) method derives a program's control structure directly and exclusively from Data Structure Diagrams of its input and output, so sequences, iterations, and selections in the data are mirrored one-for-one by sequential blocks, loops, and conditionals in the code.

### Scope & Conditions

Developed for COBOL batch-file processing; rejects top-down procedural decomposition as the starting point for program design.

### Evidence

> "JSP dictated that the control structure of a program must be derived directly and exclusively from the data structures of the input and output files it processes… The code becomes a direct, isomorphic reflection of the data structure."

### Implications

- Because requirement changes over a product's life are usually small tweaks to data structure rather than radical algorithmic shifts, a JSP-derived program changes predictably and locally when its input schema changes.

### See Also

- [[SoT - Type-Driven Development (The Torvalds Loop)]]—weak tag-cluster link: shares the theme of control structure being derived from data shape, though via types rather than diagrams; no note in the vault currently covers JSP or its Data Structure Diagrams directly.
