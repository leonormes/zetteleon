---
aliases:
  - git rebase
  - rebase
conformant: true
created: 2026-11-18T15:56:00+00:00
definition: A Git operation that replays a sequence of commits from one branch onto a new base commit, producing new commit objects with new hashes to form a linear history.
distinguishes_from:
  - "[[Git Merge Commits and Diffs]]"
modified: 2026-11-18T15:56:00+00:00
permalink: llmeon/30-library/100-zettelkasten/git-rebase
status: stable
tags:
  - domain/infrastructure
  - git
  - scm
  - version-control
title: Git Rebase
type: concept
used_in_claims:
  - "[[SoT - Git]]"
---

## Git Rebase

Rebasing (`git rebase`) takes a sequence of commits from a branch and replays them one by one onto a different base commit, creating brand-new commit snapshots and hashes. Unlike merging, which joins two histories with a merge commit, rebasing produces a clean, linear commit history at the cost of rewriting commit IDs. ^def

### Scope & Conditions

- **Local vs shared branches:** Safe and clean on unshared or personal feature branches; rewriting history on a shared branch forces collaborators to reconcile diverged hashes (`git push --force-with-lease`).
- **Interactive mode (`git rebase -i`):** Allows reordering, squashing, editing, or dropping commits before integration.

### Evidence

- Standard Git history-rewriting semantics; see `[[SoT - Git]]`. *(No Calibre book quotation attached yet.)*

### Implications

- **Readable history vs auditability:** Improves linear bisection and review clarity on feature branches, while protected mainline branches disable force-pushes so rebased history is never overwritten post-merge.

### Related

- [[SoT - Git]]—synthesises: covers rebasing in branching and commit hygiene.
- [[Git Merge Commits and Diffs]]—contrasts with: preserves branching topology via multi-parent commits instead of rewriting hashes.
