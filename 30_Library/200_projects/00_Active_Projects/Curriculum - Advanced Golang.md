---
aliases: []
benchmark_source: "Official Go Docs, 'The Go Programming Language'"
confidence: ""
created: 2025-12-24T17:16:29Z
epistemic: ""
last_reviewed: ""
modified: 2025-12-25T18:35:16Z
purpose: ""
related_project: "[[Project - Concurrent TCP Log Ingestor]]"
review_interval: ""
see_also: []
source_of_truth: []
status: Active
tags: ["backend", "curriculum", "golang", "skill_acquisition"]
title: Curriculum - Advanced Golang
type: Curriculum
uid: 
updated: 
version: 1.1
---

## Curriculum: Advanced Golang (Node Dev Perspective)

> [!mission] The Philosophy
> **Directness:** We do not study topics; we build projects.
> **The Goal:** To transition from "Async/Await" thinking to "CSP/Channels" thinking.

### 1. The Challenge (Directness)

**The Capstone Project:**

> *Build a High-Throughput Concurrent TCP Log Ingestor.*

- [ ] **Build:** A service that accepts raw log lines via TCP, buffers them, parses them concurrently, and writes batches to a file/DB.

**Definition of Done:**
- [ ] Server handles 10k concurrent connections without leaking goroutines.
- [ ] Graceful shutdown (SIGTERM) drains all active channels before exiting.
- [ ] Race detector (`go run -race`) reports zero issues.

---

### 2. Metalearning Decomposition (The Map)

> *Linked Drills must be actionable.*

| Category | Key Items (The Syllabus) | Linked Drill (The Action) |
|:--- |:--- |:--- |
| **Concepts** | **Concurrency (CSP):** Sharing memory by communicating. | *Drill:* Refactor a shared `map` using a `Mutex`, then refactor it again using a `Monitor Goroutine` (Channel). Measure the difference. |
| | **Interfaces:** Structural Typing. | *Drill:* Create a `Logger` interface. Implement it with `FileLogger` and `ConsoleLogger`. Swap them at runtime. |
| **Facts** | **Syntax:** `defer`, `panic`, `recover`. | *Drill:* Create a function that panics. Wrap it in a middleware that recovers and logs the stack trace. |
| | **Allocation:** `make` vs `new`. | *Drill:* Write a snippet that crashes by assigning to a `nil` map. Fix it using `make`. |
| **Procedures** | **Debugging:** Race Detection. | *Drill:* Intentionally write a race condition (2 goroutines incrementing an int). Run `go run -race` to catch it. |
| | **Profiling:** `pprof`. | *Drill:* Generate a CPU profile of the Ingestor under load (using `wrk` or `hey`). |

---

### 3. The Timebox Menu (The Implementation)

> [!warning] Action Required
> Select one item below and assign it a **50-minute Timebox** on your Calendar.

| Drill Name / Activity | Est. Pomodoros | Definition of Done (Output) |
|:--- |:--- |:--- |
| **Setup & Hello World** | 1 (25m) | *Go installed, VSCode configured, "Hello" prints.* |
| **The TCP Listener Drill** | 2 (50m) | *Server accepts telnet connection and echoes text back.* |
| **The Race Condition Lab** | 1 (25m) | *Race detector flags the error, then passes after Mutex fix.* |
| **Worker Pool V1** | 2 (50m) | *5 workers process 100 jobs from a channel.* |
| **Graceful Shutdown Impl** | 2 (50m) | *Server catches Ctrl+C and prints "Draining..." before exit.* |

---

### 4. Failure Mode Protocols (ADHD Support)

> *If I get stuck on the Hard Problem, I will switch to these Diffuse Mode activities:*

- **Stuck on Channels?** -> Switch to: *Typing out the "Tour of Go" syntax examples for 10 mins.*
- **Stuck on Pointers?** -> Switch to: *Drawing the memory layout (Stack vs Heap) on paper.*
- **Too Tired?** -> Switch to: *Configuring `golangci-lint` or vim keybindings.*

---

### 5. Synthesis Queue & Feedback

> [!quote] Feynman Exit
> Raw insights go here.

**Confidence Score:** `1 - 5`
