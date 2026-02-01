---
aliases: []
AoL: Work
created: 2025-12-08T00:00:00Z
last_reviewed:
modified: 2026-02-01T15:09:11+00:00
status: someday
tags: [acr, cleanup, devops, head, thinking]
title: HEAD - ACR Image Retention Strategy
type: head
updated:
---

## The Spark

> [!abstract] The Spark (Contextual Wrapper)
Task: "re set up the image delete from acr" -> "How to slim down the images stored to just the latest but not based on time".
Time-based retention deletes infrequently updated but valid "latest" images. We need a smarter way.

## My Current Model

- Problem: `ACR Purge` usually works on `last_updated` timestamp.
- Requirement: Keep the "Semantic Latest" (e.g., v1.2.3) and maybe the last N versions, regardless of age.
- Idea: Use a script or a more advanced policy that parses tags (SemVer) to decide what to keep.

## The Tension

- Risk: Deleting a production image that is old but currently running.
- Complexity: Parsing SemVer in a bash/ACR task script is fragile.
- Untagged Images: These should be easy to delete (dangling), but tagged ones are the challenge.

## The Next Test

- [ ] Research ACR built-in retention policies capabilities (are they strictly time-based?).
- [ ] Investigate `acr-cli` or third-party tools that can "keep last N versions".
