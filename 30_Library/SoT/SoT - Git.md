---
aliases: [Distributed Version Control, Git, Version Control System]
confidence: 5/5
created: 2025-12-13T00:00:00Z
epistemic: 
last-synthesis: 2025-12-13
last_reviewed: 2025-12-13
modified: 2025-12-13T13:30:38Z
purpose: To define Git as the foundational distributed version control system, detailing its data model, core concepts, essential workflows, and security principles for robust software configuration management.
related-soTs: ["[[SoT - Software Configuration Management Patterns]]"]
resonance-score: 
review_interval: 6 months
see_also: []
source_of_truth: true
status: stable
tags: ["devops", "git", "scm", "version_control"]
title: SoT - Git
type: SoT
uid: 
updated: 
---

## 1. Definitive Statement

> [!definition] Git
> Git is a **distributed version control system (DVCS)** that tracks changes in source code during software development. It emphasizes speed, data integrity, and support for distributed, non-linear workflows by treating its history as a **Directed Acyclic Graph (DAG) of immutable snapshots**.

---

## 2. Working Knowledge (Core Concepts)

### Git's Data Model: Commits as Snapshots

-   A core concept in Git is that each **commit** is a complete **snapshot** of the project's entire working directory at a specific point in time, not a series of diffs. Diffs are merely a *presentation* of the changes calculated by comparing two snapshots.
-   The **`.git` folder** is the repository itself, containing the entire object database, references (branches, tags), and configuration.
-   The commit history forms a **Directed Acyclic Graph (DAG)**. Nodes are commits, and directed edges represent parent-child relationships. Acyclicity ensures a consistent order without loops.

### Fundamental Objects

Git uses a content-addressable object database, where objects are identified by their SHA-1 (or SHA-256) hash:

1.  **Blobs:** Represent the exact content of a file. If content changes, a new blob is created.
2.  **Trees:** Represent a directory, containing pointers to blobs (files) and other trees (subdirectories).
3.  **Commits:** The top-level object, linking to a root tree (the project snapshot), metadata (author, committer, message, timestamp), and parent commit(s).

### Key Git Areas

1.  **Working Directory:** The actual files you are editing. Git detects changes here.
2.  **Index (Staging Area):** A binary file where changes are prepared for the next commit. `git add` reads files from the working directory, creates new blob objects, and updates the index to point to these blobs. It represents the *next snapshot* to be committed.
3.  **Repository (Object Database):** Stores all commits, trees, and blobs. This is the permanent record.

---

## 3. Current Understanding (Workflows & Practices)

### Basic Operations

-   **Cloning (`git clone`):** Retrieves a complete copy of the repository, including the `.git` folder and populates the working directory with files from the default branch.
    -   `--bare`: Creates a repository without a working tree, ideal for server-side repositories.
    -   `--no-checkout --sparse`: Clones history but does not unpack working directory files.
-   **Pushing (`git push`):** Transmits only the necessary objects and updates references to synchronize the remote repository with local changes. It does not copy the entire `.git` folder.
-   **Undoing Changes:**
    -   `git revert <commit-hash>`: Creates a new commit that reverses the effects of the specified snapshot, preserving history. Safe for shared repositories.
    -   `git reset --hard <commit-hash>`: Moves the current branch pointer to the specified commit, discarding all subsequent snapshots from history. Destructive; use with caution on shared branches.
    -   `git commit --amend`: Creates a new snapshot that replaces the last commit, allowing modification of its content or message.

### Commit Best Practices

-   **Structured Messages:** Adhere to a conventional commit format:

```sh
<type>(<scope>): <short summary>

<detailed description, bullet points>

Breaking Changes:
- <any breaking changes, omit section if none>

<ticket reference>
```

    -   **Types:** `feat` (new feature), `fix` (bug fix), `docs` (documentation), `style` (formatting), `refactor` (code restructuring), `test` (test changes), `chore` (maintenance).
    -   **Ticket References:** Include ticket IDs (e.g., `FFAPP-####`, `FFDATA-####`) for traceability.
-   **Clean History:** Use `git rebase -i` to combine, reorder, or edit commits before merging. Squash merges for feature branches consolidate changes into a single, well-described commit on the main branch.

### Branching & Merging

-   **Branching Strategy:** Employ short-lived feature branches that merge frequently into the mainline.
-   **Rebasing (`git rebase`):** Reapplies a series of changes from one branch onto a different base, creating *new snapshots* for each replayed commit. This results in a clean, linear history but rewrites commit history, requiring careful use in shared branches.
-   **Merge Commits:** Represents the integration of changes from multiple parent branches. Viewing its diff shows the *net result* of all combined changes since the common ancestor.

### Security & Auditability

-   **Tamper-Evident History:** Git's cryptographic hashing ensures that any change to commit history is immediately detectable, as it would alter all subsequent commit hashes in the chain.
-   **GitOps:** Leverages Git as the single source of truth for declarative configurations (infrastructure, applications) and automates deployment processes. This enables version-controlled, auditable, and repeatable deployments.
-   **GitLab's Protected Branches:** Crucial for GitOps security. These prevent `git push --force`, enforce merge request reviews and approvals, and require CI/CD status checks, making tampering difficult to go undetected.
-   **Signed Commits:** GPG or SSH signing of commits provides cryptographic proof of authorship and integrity.

---

## 4. Minimum Viable Understanding (MVU)

1.  **Git stores Snapshots, not Diffs:** Every commit is a complete copy of the project.
2.  **History is a DAG:** Branching and merging create a graph of interconnected commits.
3.  **Index is the Staging Area:** It's where you build your next snapshot.
4.  **Version Everything in Git:** Code, config, infrastructure, docs.
5.  **Clean, Atomic Commits:** Use structured messages and rebase for readable history.
6.  **Protected Branches are Key for GitOps:** Prevent history rewriting and enforce reviews.

---

## 5. Sources and Links

- [[The Fundamental Misconception Commits as Diffs]]
- [[directed acyclic graph]]
- [[dot_git folder]]
- [[git glossary]]
- [[git index]]
- [[Git Command to Clone only the git Folder]]
- [[git extended]]
- [[gitops]]
- [[Properties of a Directed Acyclic Graph]]
- [[rebase]]
- [[Understanding Merge Commits and Diffs]]
- [[undoing changes in git]]
- [[ff git process for better logs]]
- [[cicd fundamental]]
- [[efficient and effective Continuous Delivery pipeline]]
- [[Universal Keymap Plan]]
