---
aliases:
  - .git folder
  - dot_git folder
conformant: true
created: 2026-11-18T15:56:00+00:00
definition: The hidden .git directory inside a repository that houses the entire content-addressed object database, references (branches and tags), index, and local configuration.
distinguishes_from:
  - "[[Git Index (Staging Area)]]"
modified: 2026-11-18T15:56:00+00:00
permalink: llmeon/30-library/100-zettelkasten/git-repository-object-store-dot-git-folder
status: evergreen
tags:
  - domain/infrastructure
  - git
  - scm
  - version-control
title: Git Repository Object Store (.git Folder)
type: concept
used_in_claims:
  - "[[SoT - Git]]"
  - "[[Git's Content-Addressed Object Store Absorbs Distributed-Trust Complexity Into Structure]]"
---

## Git Repository Object Store (.git Folder)

The `.git` directory is the repository itself, storing the content-addressed object database (blobs, trees, commits, annotated tags), refs (`HEAD`, branches, tags), staging index, hooks, and local configuration. Unlike the working tree, which is a checked-out view of one commit, `.git` contains the complete local history. ^def

### Scope & Conditions

- **Bare vs working repositories:** A `--bare` repository is essentially the contents of `.git` without a checked-out working tree, used on servers and remotes.
- **Worktrees:** Additional `git worktree` checkouts share the main `.git/objects` store while keeping separate `HEAD` and index state.

### Evidence

- Standard Git repository layout (`objects/`, `refs/`, `HEAD`, `index`, `config`); see `[[SoT - Git]]`. *(No Calibre book quotation attached yet.)*

### Implications

- **Local autonomy:** Having the full object store inside `.git` lets commits, diffs, branching, and history inspection run offline without contacting a central server.

### Related

- [[SoT - Git]]—synthesises: core repository structure.
- [[Git's Content-Addressed Object Store Absorbs Distributed-Trust Complexity Into Structure]]—explains: how content-addressed objects absorb distributed trust.
- [[Git Index (Staging Area)]]—adjacent: `.git/index` bridges the working tree and the object store.
