---
aliases: []
confidence: 
created: 2025-12-19T10:00:00Z
epistemic: 
last_reviewed: 
modified: 2025-12-19T10:00:16Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: CLI Argument Parsing layer
type: 
uid: 
updated: 
---

You have correctly identified the symptom, but the root cause is architectural rather than regex-specific.

The issue lies in the **CLI Argument Parsing layer**, not the Rust Regex engine itself.

## The Architectural Conflict: Parser vs. Payload

When you pass a string starting with `-` (like `'-   '`) to a command-line tool, the tool's argument parser (often the `clap` library in Rust ecosystems) intercepts it before it ever reaches the regex engine. It interprets the leading hyphen as the start of a **flag** or **option** (like `-h` or `--version`), rather than a **positional argument** (your search pattern).

Your solution (`\-`) worked because the backslash prevented the parser from seeing the hyphen as the first character, allowing it to pass through to the regex engine, where `\-` is treated as a literal hyphen.

## The Canonical Solution: The Double Dash (`--`)

The standard POSIX mechanism to resolve this ambiguity is the **End of Options** delimiter: `--`. This signals to the argument parser that "everything following this delimiter is a positional argument, not a flag," regardless of whether it starts with a hyphen.

Using `--` is generally preferred over escaping because it is explicitly structural rather than syntactical.

### Implementation with `sd`

```bash
# The structural approach (Recommended)
fd -e md -x sd -- '-   ' '- '

# Your current approach (Functional, but relies on regex escaping)
fd -e md -x sd '-   ' '- '

```

## Why This Matters for Your Mental Model

- **Layer 1 (Shell):** Processes quotes and spaces.
- **Layer 2 (CLI Parser):** Scans for flags (starting with `-`). **<-- The collision happened here.**
- **Layer 3 (Regex Engine):** Compiles the pattern string.

By using `--`, you explicitly bridge Layer 2, ensuring your payload reaches Layer 3 exactly as intended without modifying the regex pattern itself.

Would you like to wrap this logic into a concise shell function for safely cleaning bullet points in the future?
