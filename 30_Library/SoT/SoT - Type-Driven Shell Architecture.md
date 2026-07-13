---
aliases: [Shell Scripting Patterns, Shell Type Safety, Unix Philosophy]
created: 2025-12-13T00:00:00+00:00
last_reviewed: '2026-03-28'
modified: 2026-07-13T08:45:23+00:00
permalink: llmeon/30-library/so-t/so-t-type-driven-shell-architecture
status: growing
tags: [architecture, automation, bash, shell, sot, unix]
title: SoT - Type-Driven Shell Architecture
type: SoT
---

## Minimum Viable Understanding (MVU)

Shell scripting is not just a collection of commands; it is a composition of concurrent processes communicating via byte streams. "Everything is a file" really means "Everything is a File Descriptor." Robust shell architecture requires treating these streams as typed (via social contract) and implementing strict error handling (`set -euo pipefail`) to bridge the gap between unstructured bytes and deterministic logic.

---

## Working Knowledge

### 1. The Stream Mechanics: Kernel Buffering

When you write `cmd1 | cmd2`, both processes are launched simultaneously.

- Concurrency: `cmd2` starts reading immediately; it does not wait for `cmd1` to finish.
- Backpressure: The pipe is a 64KB kernel buffer. If the buffer is full, `cmd1` blocks. If empty, `cmd2` blocks. This ensures a fast producer cannot overwhelm a slow consumer.
- Signals: If `cmd2` exits early, the kernel sends `SIGPIPE` to `cmd1`, terminating it.

### 2. The Universal Interface: File Descriptors (FD)

The numbered channel is the only real abstraction.

- Rewiring: Redirection (`>`, `<`, `|`) is just rewiring FDs before the process starts. The program code is identical; only the plumbing changes.
- Standard Trio: FD 0 (stdin), FD 1 (stdout), FD 2 (stderr).
- Tangible Files: Terminals, network sockets, and `/dev/null` are all "files" because they can be opened via FD.

### 3. Minimal Environment Debugging

In lean container environments where `curl`, `netcat`, or `dig` are missing, use Bash built-ins:

#### TCP Port Check (The /dev/tcp Pattern)

```bash
# Checks if example.com port 80 is open
timeout 1 bash -c "echo > /dev/tcp/example.com/80" && echo "Open" || echo "Closed"
```

#### HTTP Response Check (File Descriptor Redirection)

```bash
exec 3<>/dev/tcp/google.com/80
echo -e "GET / HTTP/1.1\r\nHost: google.com\r\nConnection: close\r\n\r\n" >&3
cat <&3
```

#### DNS Resolution

```bash
getent ahostsv4 google.com
```

---

## Current Understanding

### The "String-Only" Constraint

Variables in shell are always strings. Arithmetic (`$((…))`) and booleans are just choice-based re-interpretations.

- Filesystem as Data Structure: For complex state (queues, lookup tables), use the filesystem (`/tmp/cache/`) as your primary data structure.
- Exit Codes as Return Type: Functions only return integers (0-255). To "return" data, write to `stdout` and capture via `$()`.

### Defensive Patterns

- `set -e`: Exit on error.
- `set -u`: Exit on unset variable.
- `set -o pipefail`: Ensure pipe errors propagate correctly.
- `set -E`: Traps `ERR` in functions.

## Related Documentation

- [[SoT - Linux Networking Primitives]]
- [[SoT - Process Execution (Kernel Logic)]]
- [[5 Essential Network Debugging Commands in Minimal Linux]]
