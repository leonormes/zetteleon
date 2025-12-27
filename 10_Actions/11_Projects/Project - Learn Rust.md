---
confidence: ""
epistemic: ""
purpose: ""
modified: 2025-12-27T14:23:52+00:00
last_reviewed: ""
review_interval: ""
see_also: []
source_of_truth: []
aliases: ["Rust Learning Path", "Project - Learn Rust"]
created: 2025-12-27T12:00:00Z
status: active
tags: ["learning", "rust", "project", "prodos"]
title: "Project: Learn Rust (The Path)"
type: project
---

# Project: Learn Rust (The Path)

> [!abstract] The "Why" (Top-Down Context)
> **Goal:** To build high-performance CLI tools for ProdOS that don't crash.
> **The Problem:** Python is slow and runtime errors are annoying. Rust promises safety and speed.
> **The "Boss Fight":** Build a CLI tool that parses my Obsidian vault and finds broken links in under 100ms.

---

## 1. The Map (Curriculum)

*Don't over-plan. Unlock levels sequentially.*

### Level 1: The Basics (Syntax & Safety)

*Goal: Understand why Rust is weird.*
- [ ] **Mission 1:** Install Rust (`rustup`) and print "Hello World".
- [ ] **Mission 2:** The Variable Struggle (Mutability). Write a script that fails to compile because of `mut`.
- [ ] **Mission 3:** Ownership 101. Pass a string to a function and try to use it again (Watch it crash).
- [ ] **Boss Fight 1:** A "Guess the Number" CLI game.

### Level 2: The Borrower (Memory Model)

*Goal: Make friends with the Borrow Checker.*
- [ ] **Mission 4:** References & Borrowing. Write a function that calculates word count without taking ownership.
- [ ] **Mission 5:** Structs & Enums. Model a `TodoItem` with states (Pending, Done).
- [ ] **Boss Fight 2:** A CLI Todo app that saves to a JSON file.

### Level 3: The Builder (Real World)

*Goal: Build the Vault Parser.*
- [ ] **Mission 6:** Error Handling (`Result` & `Option`). No `.unwrap()` allowed!
- [ ] **Mission 7:** File I/O. Read a markdown file line-by-line.
- [ ] **Mission 8:** Regex in Rust. Find `[[links]]`.
- [ ] **Final Boss:** The Vault Link Checker.

---

## 2. Active Quest (The Workbench)

*Link your current HEAD note here.*
- **Current Focus:** [[2025-12-27-1200-HEAD - Rust Ownership Struggle]]

---

## 3. The Loot (Source of Truth)

*Synthesized notes go here. These are your trophies.*
- [[SoT - Rust Ownership Model]]
- [[SoT - Rust Error Handling Patterns]]

---

## 4. The Loop (How to use this note)

1. **Pick a Mission:** Select the next unchecked item.
2. **Spin Up:** Create a HEAD note (`cmd+shift+n`) to "fight" the concept.
    * *Name it:* `YYYY-MM-DD-HHmm-HEAD - Rust Borrowing`
3. **The Test:** Write the code. Fail. Fix it.
4. **Synthesize:** When you understand it, create/update an SoT note (The Loot).
5. **Level Up:** Check the box in this Project note.
