---
aliases: ["Go for DevOps", "Golang Learning Path", "Node to Go Transition"]
benchmark_source: "Official Go Docs, 'The Go Programming Language', Kubebuilder"
confidence: ""
created: 2025-12-24T17:16:29Z
epistemic: "Synthesized from Node.js -> Go transition patterns and Cloud Native architectural requirements."
last_reviewed: "2025-12-26"
modified: 2025-12-28T18:49:31+00:00
purpose: "A project-driven curriculum to transition from Node.js/TS to Cloud Native Go."
related_project: "[[Project - Concurrent TCP Log Ingestor]]"
review_interval: "3 months"
see_also: ["[[SoT - Tool - NotebookLM]]"]
source_of_truth: []
status: Active
tags: ["backend", "curriculum", "golang", "skill_acquisition", "devops"]
title: Curriculum - Advanced Golang
type: Curriculum
uid: 
updated: 
version: 2.0
---

## Curriculum: Go for Cloud Native DevOps

> [!mission] The Philosophy
> **Identity Shift:** You are not learning "Syntax"; you are re-aligning your mental model from **Event Loops (Node)** to **Scheduler/CSP (Go)**.
> **Methodology:** "Think like a Man of Action." We build 3 specific tools to master 3 specific architectural domains.

---

## 1. The Mental Shift (Node.js -> Go)

| Concept | Node/TS Mental Model | Go Mental Model | The Shift |
|:--- |:--- |:--- |:--- |
| **Concurrency** | **Async/Await** (Single Thread). Fear blocking the main thread. | **Goroutines/CSP** (M:N Scheduler). Blocking is fine; the scheduler handles it. Share memory by communicating (Channels). |
| **Types** | **Structural** (Shapes, Unions `A \| B`). | **Interfaces** (Behavior). Implicit Duck Typing. No `implements` keyword. |
| **Errors** | **Exceptions** (`try/catch`). Bubbling. | **Values** (`if err!= nil`). Explicit handling at point-of-failure. |
| **Architecture** | **Layer-First** (DB -> Controller). | **Domain-First** (Struct -> Interface). Hexagonal/Ports & Adapters. |

---

## 2. The Project Ladder (Execution)

### Level 1: The CLI (The Syntax Shift)

**Project A: "DevOps Swiss Army Knife"**
*Goal:* Replace a Bash/Node script (e.g., Log Parser, S3 Cleaner) with a binary.
*Focus:* Structs, Interfaces, `os/exec`, `flag`.

| Drill / Timebox (50m) | Definition of Done (Output) |
|:--- |:--- |
| **Setup & Hello World** | Go installed, `go.mod` init, VSCode configured. |
| **The Flag Parser** | CLI accepts flags (`--file`, `--dry-run`) using the `flag` stdlib. |
| **The Interface Drill** | Create a `Reader` interface. Implement `FileReader` and `StdinReader`. Swap them. |
| **The Executioner** | Use `os/exec` to run a system command (e.g., `grep`) and capture stdout. |

### Level 2: The Service (The Concurrency Shift)

**Project B: "Resilient Microservice / TCP Ingestor"**
*Goal:* A long-running service that manages goroutine lifecycles and timeouts.
*Focus:* Goroutines, Channels, `context.Context`, `net/http` or `net`.

| Drill / Timebox (50m) | Definition of Done (Output) |
|:--- |:--- |
| **The TCP Listener** | Server accepts telnet connection and echoes text back. |
| **The Context Lab** | Create a handler that sleeps for 5s. Cancel the request from client. Handler must stop work immediately. |
| **The Race Lab** | Write a race condition (shared map). Fix it with `sync.Mutex`. Fix it again with Channels. |
| **The Worker Pool** | 5 workers process 100 jobs from a buffered channel. Graceful shutdown on SIGTERM. |

### Level 3: The Operator (The Architecture Shift)

**Project C: "Kubernetes Custom Controller"**
*Goal:* A controller that watches a CRD and reconciles state.
*Focus:* Level-Triggered Logic, Kubebuilder, Eventual Consistency.

| Drill / Timebox (50m) | Definition of Done (Output) |
|:--- |:--- |
| **The Reconciliation Loop** | Watch a video on "Level-Triggered Logic". Draw the `Observe -> Compare -> Act` loop. |
| **The Scaffold** | Use `kubebuilder` to generate a project structure. Explore `api/` and `internal/controller/`. |
| **The CRD Def** | Define a `Database` struct in Go. Generate the YAML CRD. Apply it to a Kind cluster. |

### Level 4: The Architect (Domain-First Design)

**Project D: "Mini-Vault" (The Hexagonal Challenge)**
*Goal:* Build a secure Key-Value store using TDD and "Core-Out" design.
*Focus:* Dependency Inversion, TDD, Encryption.

| Drill / Timebox (50m) | Definition of Done (Output) |
|:--- |:--- |
| **The Domain Core** | Define `Secret` struct and `SecretStore` interface. No imports allowed. |
| **The Mock Test** | Write a `MockStore`. Write a TDD test for `VaultService` that passes. |
| **The Adapter** | Implement `FileStore` or `K8sStore` that satisfies the interface. |

---

## 3. Failure Mode Protocols (ADHD Support)

> *If I get stuck on the Hard Problem, I will switch to these Diffuse Mode activities:*

- **Stuck on Architecture?** -> Switch to: *Drawing the "Nouns" (Structs) and "Verbs" (Interfaces) on paper.*
- **Stuck on Concurrency?** -> Switch to: *The "Race Condition Lab" drill. Break things intentionally.*
- **Stuck on Syntax?** -> Switch to: *Typing out "Tour of Go" examples physically (Muscle Memory).*
- **Overwhelmed?** -> Switch to: *Configuring `golangci-lint` or reading `go.mod` docs.*

---

## 4. Synthesis & Resources

- **Book:** "The Go Programming Language" (Donovan/Kernighan) - *Chapters 1, 8, 9.*
- **Video:** [Master of Resources: Building Kubernetes Operators in Go](https://www.youtube.com/watch?v=uJlGa3ygiBI)
- **Pattern:** **Hexagonal Architecture** (Ports & Adapters).
