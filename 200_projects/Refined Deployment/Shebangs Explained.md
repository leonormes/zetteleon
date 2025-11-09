---
aliases: []
confidence: 
created: 2025-11-03T11:25:15Z
epistemic: 
last_reviewed: 
modified: 2025-11-03T15:37:41Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: Shebangs Explained
type: 
uid: 
updated: 
---

**Key Takeaways — "Why I Don't Use \#!/bin/bash - Shebangs Explained!"**

- **Shebang location matters:**
`/bin/bash` is not guaranteed to exist or be the correct bash version on every system; hardcoding this path can break scripts on OS X, Linux distros with Homebrew, NixOS, voids, etc.
Using `#!/usr/bin/env bash` is more portable, since it finds `bash` as defined by the user's `PATH` variable.[^1_1]
- **Bash version issues:**
Mac ships with a very old (3.2) version of Bash at `/bin/bash`, which lacks modern features like associative arrays.
Relying on the environment's version (via `env`) means you get the user's preferred or updated bash, not an ancient system-installed one.[^1_1]
- **The shebang is OS-dependent:**
Shebang lines tell the kernel how to launch the script:
    - Linux: only one argument after the interpreter is supported
    - macOS/Darwin: supports multiple arguments
    - Illumos/OpenSolaris: throws out extra arguments past the first
Don't rely on passing multiple interpreter arguments via shebangs—most systems don't support it; `env -S` (split) exists on GNU/Linux and macOS, but not all OSes.[^1_1]
- **Security implications:**
Using `env` means the interpreter is resolved according to user `PATH`, which can be hijacked for supply-chain or privilege attacks; using `/bin/bash` is more static, but less flexible.[^1_1]
- **Best practice:**
If you want **maximum portability** (especially in scripts shared online, across repo/teams, or for devops use):
    - Prefer `#!/usr/bin/env bash`
    - Accept you can't guarantee interpreter location or version
    - If your environment is fixed/known (e.g., 100 identical hosts), hardcoding is safe
- **Special cases:**
    - For Python, `#!/usr/bin/env python3` lets you leverage virtual environments
    - Some minimal systems (rescue images, embedded systems) might lack both bash and env[^1_1]
    - Shebang is strictly interpreted by the kernel loader—not a “hint”, but a set system call[^1_1]
- **Bonus tricks:**
    - You can override `argv[^1_0]` with the `exec -a` shell built-in, changing program behavior based on its apparent name (Busybox uses this to expose many utilities from a single binary)
    - Interpreter-supplied comments (`# ...`) in languages like JavaScript rely on the engine to strip out the shebang line when not using shell scripts

**Summary Table**

| Shebang Style | Use Case | Pros | Cons/Warnings |
| :-- | :-- | :-- | :-- |
| \#!/bin/bash | Fixed system env, legacy scripts | Predictable version | Not portable, version issues |
| \#!/usr/bin/env bash | Cross-platform/devops/distributed | Portable, user PATH | PATH security risk, relies on env location |
| \#!/usr/bin/env python3 | Python/venv-friendly scripts | Venv support | Can break on minimal systems |
| \#!/bin/sh | Max. portability, POSIX compliance | Universal, minimal | No Bash-specific features |

**Action Item:**

- Use `#!/usr/bin/env bash` for scripts intended to work everywhere. Fall back to `/bin/bash` (or `/bin/sh`) if you control the run environment, or need strict stability for system scripts.

<div align="center">⁂</div>

[^1_1]: <https://www.youtube.com/watch?v=aoHMiCzqCNw>
