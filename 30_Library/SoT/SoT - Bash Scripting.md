---
aliases: ["Bash Scripting", "Shell Scripting", "Bash Arrays"]
confidence: "5/5"
created: 2025-12-26T12:00:00Z
epistemic: "Verified via practical examples"
last_reviewed: "2025-12-26"
modified: 2025-12-26T10:08:15+00:00
purpose: "Canonical knowledge regarding Bash scripting patterns, best practices, and pitfalls."
review_interval: "6 months"
see_also: ["[[SoT - Process Execution (Kernel Logic)]]"]
source_of_truth: ["[[Bash for loops confused me until I learned these 4 expansion rules]]", "[[Kernel Hints and Path Resolution]]"]
status: "stable"
tags: ["programming", "topic/linux", "bash", "scripting"]
title: SoT - Bash Scripting
type: "SoT"
uid: 
updated: 
---

## 1. Definitive Statement

> [!definition] Definition
> **Bash (Bourne Again SHell)** is the default command-line interpreter and scripting language for most Linux distributions and macOS. It excels at process orchestration and file manipulation but requires strict adherence to quoting rules to avoid "Word Splitting" errors.

## 2. Working Knowledge (Stable Foundation)

### Core Philosophy: "Everything is a String (Mostly)"

Bash treats most inputs as strings separated by whitespace. This makes it powerful for text processing but dangerous when filenames or data contain spaces.

### Portable Execution (The Shebang)

For a Bash script to be portable across different Unix systems (Linux, macOS, BSD), use the `env` utility to locate the interpreter.

- **Recommended Shebang:** `#!/usr/bin/env bash`
- **Why:** This avoids hardcoding `/bin/bash`, which may be an outdated version (macOS) or located in a different path (Homebrew, NixOS).
- **Deep Dive:** See **[[SoT - Process Execution (Kernel Logic)]]** for how the kernel interprets this line.

## 3. Current Understanding (Coherent Narrative)

### Array Expansion & Quoting Rules

The behavior of Bash arrays changes drastically based on **Quoting** and the **Expansion Operator** (`@` vs `*`).

| Syntax | Expansion Result | Word Splitting? | Use Case |
|:--- |:--- |:--- |:--- |
| `"${arr[@]}"` | **Elements Preserved** | **NO** | **Safe iteration.** The default for almost all loops. |
| `${arr[@]}` | Words Split | **YES** | Dangerous. Splits "one two" into "one", "two". |
| `"${arr[*]}"` | Single String | **NO** | Joins all elements into one long string. |
| `${arr[*]}` | Words Split | **YES** | Redundant. Same behavior as `${arr[@]}`. |

#### The Mechanism: Word Splitting

When unquoted, Bash performs **Word Splitting** on expanded values using the characters defined in `$IFS` (Internal Field Separator).

- **Default `$IFS`:** Space, Tab, Newline.
- **Consequence:** An array element like `"File Name.txt"` becomes two items: `"File"` and `"Name.txt"`.

#### Example: The "For Loop" Trap

```bash
my_arr=("one a" "two b")

# ❌ BAD: Word Splitting occurs
# Output: "one", "a", "two", "b"
for item in ${my_arr[@]}; do
  echo "$item"
done

# ✅ GOOD: Elements preserved
# Output: "one a", "two b"
for item in "${my_arr[@]}"; do
  echo "$item"
done
```

## 4. Minimum Viable Understanding (MVU)

> [!check] The Golden Rule
> **Always double-quote your array expansions: `"${array[@]}"`**.
> Only omit quotes if you *explicitly intend* to split strings by whitespace.

## 5. Tensions, Gaps, and Cross-SoT Coherence

- **Tension:** Bash's syntax prioritizes interactive convenience (less typing) over scripting safety (implicit splitting), leading to "gotchas" in scripts.
- **Gap:** Need to expand this SoT to cover `mapfile` for safe reading of lines into arrays.
