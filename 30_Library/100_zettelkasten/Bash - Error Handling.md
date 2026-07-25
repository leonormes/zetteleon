---
conformant: false
created: 2026-02-10T00:00:00+00:00
modified: 2026-07-21T09:15:03+00:00
non_conformance_reason: Bulk inferred type. Needs review.
permalink: llmeon/30-library/100-zettelkasten/bash-error-handling
tags:
  - bash
  - devops
  - reference
  - shell
title: Bash - Error Handling
type: procedure
---

## Bash Error Handling

### The Core Principle

Every command returns an exit code. `0` means success. Anything else means failure. This is the foundation of all bash error handling.

```sh
ls /real-path
echo $?  # 0 (success)

ls /nonexistent-path
echo $?  # 1 (failure — non-zero)
```

#### Notable Reserved Exit Codes

| Code  | Meaning                        |
| ----- | ------------------------------ |
| `0`   | Success                        |
| `1`   | General error                  |
| `126` | Permission denied (not executable) |
| `127` | Command not found              |
| `130` | Terminated by Ctrl+C           |

> [!info] Many programmes define their own codes (e.g. `curl` returns `6` for DNS failure, `28` for timeout). Always check docs for the tool you're using.

---

### The Dangerous Default

Bash does NOT stop on failure by default. If a command fails, bash just moves to the next line. This is unlike most programming languages and is the root cause of most bash footguns.

```sh
#!/bin/bash
rm important-lockfile.txt    # fails silently if file doesn't exist
deploy_application            # runs anyway — potentially dangerous
```

---

### The Safety Net: `set` Options

Place this at the top of every script, right after the shebang:

```sh
#!/bin/bash
set -eEuo pipefail
```

| Flag             | What It Does                                      |
| ---------------- | ------------------------------------------------- |
| `-e`             | Exit immediately on any uncaught non-zero exit code |
| `-E`             | Inherit `ERR` traps into functions and subshells   |
| `-u`             | Treat unset/undefined variables as errors          |
| `-o pipefail`    | Fail the whole pipe if _any_ command in it fails   |

> [!warning] `-e` has a caveat: it exits _before_ you can capture `$?`. If you need to inspect the exit code, use an `if` block instead (see below).

---

### Error Catching Techniques

#### 1. `||` Operator—Quick Inline Fallbacks

Runs the second command only if the first fails. Best for one-liner recovery.

```sh
# Log to stderr on failure
curl https://api.example.com/health || echo "Health check failed" >&2

# Exit with a message
cd /deploy/dir || { echo "Deploy dir missing, aborting." >&2; exit 1; }
```

#### 2. `if/else`—When You Need Granularity

Use when you need to distinguish between _different_ failure modes or do multi-step recovery.

```sh
some_command
rc=$?

if [ $rc -eq 0 ]; then
    echo "All good."
elif [ $rc -eq 1 ]; then
    echo "Known failure — retrying..." >&2
    retry_command
elif [ $rc -eq 2 ]; then
    echo "Fatal config error — aborting." >&2
    exit 2
else
    echo "Unexpected exit code: $rc" >&2
    exit $rc
fi
```

Useful comparison operators: `-eq` (equal), `-ne` (not equal), `-gt` (greater than).

> [!warning] If `-e` is set, the script will exit on `some_command` before you reach `rc=$?`. Disable `-e` temporarily or wrap in `if` directly:
>
> ```sh
> if some_command; then
>     echo "success"
> else
>     echo "failed with $?"
> fi
> ```

#### 3. `trap`—Global Error Handler

Catches any unhandled `ERR` signal. Think of it as a top-level `catch` block. Declare it once, early.

```sh
#!/bin/env bash
set -eEuo pipefail

cleanup() {
    echo "ERROR on line $1 of $(basename "$0")" >&2
    # Add cleanup logic here: remove temp files, release locks, etc.
}

trap 'cleanup $LINENO' ERR

# -- rest of your script --
download_data
process_data      # if this fails, cleanup() fires automatically
upload_results
```

> [!tip] The `-E` flag is essential here—without it, `trap ERR` won't fire inside functions or subshells.

---

### The Three Pitfalls

#### 1. Pipes Hide Failures

By default, only the last command's exit code matters in a pipe.

```sh
cat missing-file.txt | wc -l
echo $?  # 0 — wc succeeded, bash doesn't care that cat failed!
```

Fix: `set -o pipefail` makes the pipe return the exit code of the first failing command.

```sh
set -o pipefail
cat missing-file.txt | wc -l || echo "Pipeline failed!" >&2
```

#### 2. Undefined Variables Silently Expand to Empty

```sh
USER_ID=$(grep "user_id" config.txt)  # config.txt doesn't exist
echo "Deleting user $USER_ID"          # Deletes... nothing? Or everything?
```

Fix: `set -u` makes this an immediate error. For manual checks:

```sh
# -z tests for empty string
if [ -z "$USER_ID" ]; then
    echo "USER_ID is empty — aborting" >&2
    exit 1
fi
```

#### 3. Forgetting to Alert on Failure

Scripts running as cronjobs can fail silently for weeks. Always pair error handling with alerting.

```sh
# Slack webhook on failure
database_backup.sh || curl -sS -X POST \
  -H "Content-Type: application/json" \
  -d '{"text":"⚠️ DB backup failed on '"$(hostname)"'"}' \
  "$SLACK_WEBHOOK_URL"
```

---

### Decision Guide: Which Technique When?

| Situation                                    | Use               |
| -------------------------------------------- | ----------------- |
| Quick fallback / one-liner recovery          | `\|\|` operator   |
| Need to distinguish between exit codes       | `if/else` + `$?`  |
| Multi-step error recovery                    | `if/else` block   |
| Global "catch-all" for unexpected failures   | `trap ERR`        |
| All of the above as a baseline               | `set -eEuo pipefail` |

---

### Starter Template

```sh
#!/bin/env bash
set -eEuo pipefail

on_error() {
    echo "FATAL: Error on line $1" >&2
    # optional: send alert, clean up temp files, etc.
    exit 1
}

trap 'on_error $LINENO' ERR

# -- your script starts here --
```

Copy this into every new shell script as your baseline.
