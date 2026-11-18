---
aliases:
  - Merge Commits
  - Understanding Merge Commits and Diffs
conformant: true
created: 2026-11-18T15:56:00+00:00
definition: A commit with two or more parent commits that joins diverged branches in the Git DAG, whose effective diff shows the net changes relative to the first parent or common ancestor.
distinguishes_from:
  - "[[Git Rebase]]"
modified: 2026-11-18T15:56:00+00:00
permalink: llmeon/30-library/100-zettelkasten/git-merge-commits-and-diffs
status: stable
tags:
  - domain/infrastructure
  - git
  - scm
  - version-control
title: Git Merge Commits and Diffs
type: concept
used_in_claims:
  - "[[SoT - Git]]"
---

## Git Merge Commits and Diffs

A merge commit is a commit node in the Git DAG with two (or more) parents, recording the exact point where diverged branches were reconciled into a unified tree snapshot. Inspecting a merge against its first parent (`git diff HEAD^1..HEAD`) or common ancestor (`git diff main...feature`) reveals the net effect of the integrated branch rather than a single linear patch. ^def

### Scope & Conditions

- **Fast-forward vs true merge:** When the target branch has no new commits since divergence, Git can fast-forward the branch pointer without creating a merge commit (`--no-ff` forces one to preserve branch context).
- **Squash merge:** Combines a branch's changes into a single single-parent commit on the target branch, omitting the second-parent DAG link.

### Evidence

- Standard Git DAG and three-way merge semantics; see `[[SoT - Git]]`. *(No Calibre book quotation attached yet.)*

### Implications

- **Preserves topology:** Retains exact integration points for `git log --first-parent` and safe `git revert -m 1` rollbacks without rewriting shared commit hashes.

### Related

- [[SoT - Git]]—synthesises: branching and merging model.
- [[Git Rebase]]—contrasts with: rewrites commits linearly instead of creating a multi-parent node.
- [[Directed Acyclic Graph (DAG)]]—underlies: multi-parent commits form the branching DAG.
