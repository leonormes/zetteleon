---
created: 2026-04-02T10:05:00+01:00
last-synthesis: 2026-04-02
modified: 2026-04-02T10:05:00+01:00
source_of_truth: true
status: evergreen
synthesis-count: 1
tags: [domain/software-engineering, testing/tdd, theory/software-craftsmanship, ai/guardrails, type/SoT]
title: SoT - Test-Driven Development
trust-level: stable
---

## Minimum Viable Understanding (MVU)

Test-Driven Development (TDD) is a disciplined engineering practice where tests are written before implementation to define requirements and ensure testability. Beyond simple verification, TDD serves as a design tool for **evolutionary architecture**, a filter for **accidental complexity**, and a critical guardrail for **AI-assisted development**. Its core cycle is Red (Fail), Green (Pass), Refactor (Clean).

## Working Knowledge

### 1. The Red-Green-Refactor Cycle
- **Red:** Write a small, failing test defining desired behavior.
- **Green:** Write the *minimum* code necessary to make the test pass. (YAGNI principle).
- **Refactor:** Clean the code design while keeping tests green. Apply SOLID, DRY, and design patterns only as needed.

### 2. The Discipline of Proof (Dijkstra)
Tests are a form of living documentation. They establish a hierarchy of postulates, proving the code's validity by demonstrating that the code's implementation satisfies its hypothetical requirements.

### 3. Feedback Loops: The First User
"A test is the first user of your code" (Hunt & Thomas). If a test is difficult to write, the API is difficult to use. TDD forces intuitive interface design by starting from the client's perspective.

### 4. Accidental vs. Essential Complexity (Fred Brooks)
- **Essential Complexity:** The inherent difficulty of the problem.
- **Accidental Complexity:** Complexity created by poor design or bloat.
TDD acts as a filter, straining out unnecessary abstractions by focusing only on the code required to pass the test.

## Current Understanding

### AI Guardrails and the Future of Orchestration
In the era of AI-assisted coding, TDD provides the deterministic exit criteria necessary to prevent "AI Slop." By instructing agents (e.g., Claude Code) to write tests first, we provide the guardrails to ensure minimal, verified implementations.

- **Hypothesis-Driven Development:** TDD acts as a laboratory to validate architectural assumptions (e.g., choosing between an internal library or a microservice) before full implementation.
- **ATDD (Acceptance TDD):** The natural evolution for agentic orchestration. Unit tests handle the *how*; ATDD defines the *what* and *why* from a business perspective, providing the primary interface for managing agentic teams.

## Related Knowledge
- **Methodology:** [[SoT - Type-Driven Development (The Torvalds Loop)]] (`rel:: variant`)
- **Theory:** [[SoT - Infrastructure Complexity]] (`rel:: supports`)
- **Philosophy:** [[SoT - Simple Made Easy (Rich Hickey)]] (`rel:: supports`)
- **SDLC:** [[SoT - Accelerate & DORA]]
