---
captured: 2026-01-22T20:38:31+00:00 2026-01-22T20:38:31+00:00
created: 2026-01-22T20:38:34+00:00
modified: 2026-01-22T20:38:52+00:00
source: https://github.com/JB63134/bash_ct
status: processing
tags:
  - input
title: HEAD JB63134bash_ct ct (Command Trace) is a Bash command resolution tracer that explains how Bash resolves a command and what the kernel ultimately executes. Exposes shadowing and overridden commands.
type: head
---

## Phase 1: Ingestion (The Stream)

> [!abstract] Context
> ct (Command Trace) is a Bash command resolution tracer that explains how Bash resolves a command and what the kernel ultimately executes. Exposes shadowing and overridden commands. - JB63134/bash_ct: ct (Command Trace) is a Bash command resolution tracer that explains how Bash resolves a command and what the kernel ultimately executes. Exposes shadowing and overridden commands.

### Raw Output / Content

**[bash_ct](https://github.com/JB63134/bash_ct)** Public

ct (Command Trace) is a Bash command resolution tracer that explains how Bash resolves a command and what the kernel ultimately executes. Exposes shadowing and overridden commands.

[MIT license](https://github.com/JB63134/bash_ct/blob/main/LICENSE)

[Open in github.dev](https://github.dev/) [Open in a new github.dev tab](https://github.dev/) [Open in codespace](https://github.com/codespaces/new/JB63134/bash_ct?resume=1)## bash_ct

`ct` (Command Trace) is a Bash command resolution tracer that explains **how Bash resolves a command** and **what the kernel ultimately executes**.

It traces the full resolution process—covering aliases, functions, keywords, builtins, and external executables—while exposing shadowed commands, overrides, and filesystem indirection.

`ct` combines and extends `type`, `which`, `command -v`, and `file`, providing visibility into Bash resolution order, `$PATH` shadowing, and kernel execution details.

---

- Bash resolution order for aliases, functions, keywords, builtins, and executables
- Shadowed commands and overrides (e.g. aliases or functions hiding binaries)
- Full `$PATH` scan, including shadowed or unreachable entries
- Clear separation of **Bash resolution targets** vs **kernel execution targets**
- Filesystem execution details:
	- Canonical executable paths
	- Symlink chains (including `/etc/alternatives`)
	- ELF interpreters for binaries
	- Shebangs for scripts
- Optional JSON output for scripting and automation

`ct` is intended for understanding **why** a command resolves the way it does—not just **what** it resolves to.

---

- Traces Bash command resolution for aliases, functions, keywords, builtins, and executables
- Shows Bash vs kernel execution targets
- Highlights shadowed commands and overrides
- Performs a full `$PATH` scan, including shadowed or unreachable entries
- Detects builtin state (enabled vs disabled)
- Resolves filesystem details: canonical paths, symlink chains, `/etc/alternatives`, usr-merged directories, ELF interpreters, shebangs
- Safely auto-extends `$PATH` to include admin/system directories
- Supports `-x` / `--extend` for manual path extension
- Handles edge cases: reserved keywords, special characters
- Produces color-coded, human-readable output
- Optional JSON output for scripting and automation
- Supports tab completion
- Preserves shell environment state
- Compatible with gnu-utils and Bash ≥ 4.4
- Works in both interactive shells and scripts

---

## JSON Output

JSON output is intended for scripting and inspection.

### Notes

- Fields may be added in future versions
- Consumers should not assume strict schema stability across major versions
- `null` indicates "not applicable"
- Boolean fields are always `true` or `false`

### PATH Entries

Each PATH entry reports:

- Directory
- State (`notfound`, `file`, `symlink`)
- Symlink target (if applicable)
- Shadowed status
- `/usr` -merge detection

---

## Requirements

**Core dependencies**

- `grep`, `file`, `cut`, `head`, `readlink`, `readelf`, `awk`

**Optional (for color output)**

- `tput`

**Bash version**

- Bash ≥ 4.4

---

## Installation

Clone the repository.

```
# Clone the repository.
git clone https://github.com/JB63134/bash_ct.git /usr/local/bin/bash_ct

# Source the main script in your .bashrc or .bash_profile
echo "source /usr/local/bin/bash_ct/.bash_ct" >> ~/.bashrc

# Apply changes immediately
source ~/.bashrc
```

---

## Usage

```
ct [options] command
```

### Options

| Option | Description |
| --- | --- |
| `-h`, `--help` | Show usage information |
| `-v`, `--version` | Show version and license |
| `-j`, `--json` | Emit JSON output |
| `-x`, `--extend` | Extend `$PATH` manually |

---

## Examples

```
ct ls
ct python
ct -j bash
```

Invalid paths are rejected:

```
ct /bin/ls
ct ./script
```

---

[![awk](https://github.com/JB63134/bash_ct/raw/main/images/awk.png)](https://github.com/JB63134/bash_ct/blob/main/images/awk.png) [![mawk](https://github.com/JB63134/bash_ct/raw/main/images/mawk.png)](https://github.com/JB63134/bash_ct/blob/main/images/mawk.png) [![cd](https://github.com/JB63134/bash_ct/raw/main/images/cd.png)](https://github.com/JB63134/bash_ct/blob/main/images/cd.png) [![cd2](https://github.com/JB63134/bash_ct/raw/main/images/more_cd.png)](https://github.com/JB63134/bash_ct/blob/main/images/more_cd.png) [![which](https://github.com/JB63134/bash_ct/raw/main/images/which.png)](https://github.com/JB63134/bash_ct/blob/main/images/which.png)

## Releases

No releases published

## Packages

No packages published

## Languages

- [Shell 96.7%](https://github.com/JB63134/bash_ct/search?l=shell)
- [Roff 3.3%](https://github.com/JB63134/bash_ct/search?l=roff)

---

## Phase 2: The Gate (4D Filter)

- [ ] **Do:** < 2 mins?
- [ ] **Delegate:** Who?
- [ ] **Defer:** Move to Hangar or SoT?
- [ ] **Delete:** Is this noise?

---

## Phase 5: The Scribe (#SAVESTATE)

- **The Conflict:**
- **The Current State:**
- **The Next Test:**
