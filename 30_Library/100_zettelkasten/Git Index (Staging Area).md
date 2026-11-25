---
aliases:
  - Staging Area
  - git index
conformant: true
created: 2026-11-18T15:56:00+00:00
definition: A binary file (.git/index) sitting between the working directory and the repository object store that records the exact tree snapshot staged for the next commit.
distinguishes_from:
  - "[[Git Repository Object Store (.git Folder)]]"
modified: 2026-11-18T15:56:00+00:00
permalink: llmeon/30-library/100-zettelkasten/git-index-staging-area
status: evergreen
tags:
  - domain/infrastructure
  - git
  - scm
  - version-control
title: Git Index (Staging Area)
type: concept
used_in_claims:
  - "[[SoT - Git]]"
---

## Git Index (Staging Area)

The Git index (`.git/index`) is the staging area between the working directory and the permanent object database, holding an ordered list of file paths, modes, and blob hashes that represent the exact snapshot to be written by the next `git commit`. Running `git add` hashes working-tree files into blobs and updates the index without yet creating a commit. ^def

### Scope & Conditions

- **Three-tree boundary:** Sits between `HEAD` (last committed tree) and the working directory; `git diff` compares working tree vs index, while `git diff --staged` compares index vs `HEAD`.
- **Merge state:** During a conflicted merge, the index temporarily stores multiple stages (base, ours, theirs) per conflicted path until resolved.

### Evidence

- Standard Git three-tree architecture; see `[[SoT - Git]]`. *(No Calibre book quotation attached yet.)*

### Implications

- **Atomic commits:** Enables partial staging (`git add -p`) so unrelated edits in the working directory can be split into clean, single-purpose commits.

### Related

- [[SoT - Git]]—synthesises: defines the three key Git areas.
- [[Git Repository Object Store (.git Folder)]]—contains: `.git/index` lives inside `.git` and points to blobs in `.git/objects`.
