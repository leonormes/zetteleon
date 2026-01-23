---
aliases: ["argv[0]", "Kernel Hints", "Process Execution", "Shebang Logic"]
confidence: "5/5"
created: 2025-12-26T12:30:00Z
epistemic: "Architectural/Technical"
last_reviewed: "2025-12-26"
modified: 2026-01-23T18:09:18+00:00
purpose: "Canonical knowledge on how the OS kernel executes binaries and scripts, specifically covering path resolution and interpreter hints."
review_interval: "6 months"
see_also: ["[[SoT - Bash Scripting]]", "[[SoT - Linux Container Primitives]]"]
source_of_truth: ["[[Kernel Hints and Path Resolution]]"]
status: "stable"
tags: ["kernel", "operating-systems", "programming", "SoftwareEngineering/Linux"]
title: SoT - Process Execution (Kernel Logic)
type: "SoT"
uid: 
updated: 
---

## 1. Definitive Statement

> [!definition] Definition
> **Process Execution** in Unix-like systems is the mechanism by which the kernel transitions from a file on disk to a running process in memory. This process is orchestrated via the `exec` family of system calls, which replace the current process image with a new one, guided by **Kernel Hints** (Shebangs) and **Argument Vectors** (`argv`).

## 2. Working Knowledge (Stable Foundation)

### A. The Shebang (`#!`) as a Kernel Hint

The shebang is not a shell command; it is a magic number read by the **kernel** at the start of an executable file.

- **Kernel Action:** When the kernel sees `#!`, it stops trying to execute the file as a binary and instead launches the program specified on the shebang line, passing the original file as the final argument.

### B. The `argv` Array

- **`argv[0]`:** Conventionally the name of the program.
- **Polymorphism:** Some binaries (e.g., `bash`, `busybox`, `multi-call binaries`) change their behavior based on `argv[0]`. For example, Bash acts as a POSIX-compliant shell if launched as `sh`.

## 3. Current Understanding (Coherent Narrative)

### Path Resolution & Portability (`env` vs. Static)

Hardcoding paths (e.g., `#!/bin/bash`) is fragile due to filesystem diversity (macOS vs. NixOS vs. Debian).

| Strategy | Path | Pros | Cons |
|:--- |:--- |:--- |:--- |
| **Static** | `#!/bin/bash` | Deterministic. | Fails if binary is elsewhere (e.g., Homebrew `/opt/homebrew/bin/bash`). |
| **Dynamic** | `#!/usr/bin/env bash` | **Portable.** Uses `$PATH` to find the user's preferred version. | Slight overhead; relies on `/usr/bin/env` existence (standard in POSIX). |

### OS-Specific Shebang Handling

Different kernels parse the shebang line with varying logic regarding multiple arguments:

- **Linux (GNU/Linux):** Treats everything after the first space as a **single string**.
    - _Problem:_ `#!/usr/bin/env bash -x` might fail because Linux looks for a binary named `env bash -x`.
    - _Solution:_ GNU `env` provides the `-S` (split-string) flag: `#!/usr/bin/env -S bash -x`.
- **macOS (Darwin):** Natively supports multiple discrete arguments in the shebang.
- **SunOS (Solaris):** Discards all arguments after the first one.

## 4. Minimum Viable Understanding (MVU)

> [!check] Best Practice
> **Use `#!/usr/bin/env <interpreter>` for maximum portability.**
> Understand that the kernel, not the shell, decides how to start your script based on that first line.

## 5. Tensions, Gaps, and Cross-SoT Coherence

- **Tension:** Portability (`env`) vs. Security (Predictability). Dynamic path resolution can be hijacked by modifying `$PATH`.
- **Coherence:** This logic sits beneath the **[[SoT - Linux Container Primitives]]**, as container runtimes use the same `exec` mechanisms to launch processes inside namespaces.
