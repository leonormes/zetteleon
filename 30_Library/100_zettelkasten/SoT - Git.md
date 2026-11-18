---
aliases:
  - Distributed Version Control
  - Git
  - Version Control System
conformant: true
created: 2025-12-13T00:00:00+00:00
modified: 2026-11-18T15:56:00+00:00
permalink: llmeon/30-library/so-t/so-t-git
see_also:
  - "[[SoT - Software Configuration Management Patterns]]"
status: stable
tags:
  - domain/infrastructure
  - git
  - scm
  - version_control
title: SoT - Git
type: sot
---

## 1. Minimum Viable Understanding (MVU)

1. **Git stores snapshots, not diffs:** Every commit is a complete snapshot of the project tree; diffs are computed between snapshots.
2. **History is a DAG:** Branching and merging form a Directed Acyclic Graph of immutable, hash-addressed commits.
3. **The index is the staging area:** `.git/index` is where you compose the next snapshot before committing.
4. **Version everything in Git:** Code, configuration, infrastructure-as-code, and documentation.
5. **Clean, atomic commits:** Use structured messages and local rebasing for readable history, while protecting shared mainline branches.

---

## 2. Core Definitions & Data Model

### Git's Data Model: Commits as Snapshots

- Each commit is a complete snapshot of the project's working directory at a point in time, not a series of diffs.
- Fundamental content-addressed objects (SHA-1 / SHA-256):
  1. **Blobs:** Exact file contents.
  2. **Trees:** Directory listings pointing to blobs and sub-trees.
  3. **Commits:** Root tree pointer, author/committer metadata, message, and parent commit hash(es).

![[Git Repository Object Store (.git Folder)#^def]]

![[Directed Acyclic Graph (DAG)#^def]]

![[Git Index (Staging Area)#^def]]

---

## 3. Workflows & Practices

### Basic Operations

- **Cloning (`git clone`):** Retrieves the `.git` object store and checks out the default branch (`--bare` omits the working tree for remotes; `--no-checkout --sparse` fetches history without unpacking all files).
- **Pushing (`git push`):** Sends only missing objects and updates remote refs.
- **Undoing changes:**
  - `git revert <commit-hash>`: Appends an inverse commit, preserving history (safe on shared branches).
  - `git reset --hard <commit-hash>`: Moves the branch pointer and discards subsequent snapshots (destructive on shared branches).
  - `git commit --amend`: Replaces the tip commit with a new snapshot.

### Commit Best Practices

```sh
<type>(<scope>): <short summary>
<detailed description, bullet points>
Breaking Changes:
- <any breaking changes, omit section if none>
<ticket reference>
```

- **Types:** `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`.
- **Clean history:** Use `git rebase -i` to tidy local feature commits before merging, or squash-merge into mainline.

### Branching, Rebasing & Merging

- Employ short-lived feature branches that integrate frequently into mainline.

![[Git Rebase#^def]]

![[Git Merge Commits and Diffs#^def]]

### Security & Auditability

- **Tamper-evident history:** Cryptographic parent hashing detects any retroactive alteration of commit history.
- **GitOps:** Uses Git as the single source of truth for declarative infrastructure and application delivery ([[SoT - GitOps for Privileged Identity Management]], [[SoT - GitOps for IAM and Permissions]]).
- **Protected branches & signed commits:** Block `git push --force`, enforce MR approvals and CI/CD checks, and sign commits with GPG or SSH keys.

---

## 4. Sources and Links

- [[Directed Acyclic Graph (DAG)]]—_Defines the cycle-free commit graph underpinning Git history._ [synthesizes:: [[Directed Acyclic Graph (DAG)]]]
- [[Git Repository Object Store (.git Folder)]]—_Defines the `.git` directory, object store, and bare/worktree layouts._ [synthesizes:: [[Git Repository Object Store (.git Folder)]]]
- [[Git Index (Staging Area)]]—_Defines the `.git/index` staging boundary between working tree and repository._ [synthesizes:: [[Git Index (Staging Area)]]]
- [[Git Rebase]]—_Defines linear history replay and its shared-branch trade-offs._ [synthesizes:: [[Git Rebase]]]
- [[Git Merge Commits and Diffs]]—_Defines multi-parent merge nodes and first-parent vs ancestor diffs._ [synthesizes:: [[Git Merge Commits and Diffs]]]
- [[Git's Content-Addressed Object Store Absorbs Distributed-Trust Complexity Into Structure]]—_Claim explaining how Git's object model absorbs distributed-trust complexity._
- [[Directed Acyclic Graphs for Action Sequences Are Directed Acyclic and Graph-Structured]]—_Parallel application of DAG properties to action sequences._
- [[SOT - CI-CD Pipelines]]—_CI/CD and continuous delivery pipeline architecture._
