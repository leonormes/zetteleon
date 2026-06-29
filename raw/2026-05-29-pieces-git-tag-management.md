---
title: Git Tag Management & ArgoCD Tag Move
created: 2026-05-29 11:00:59+00:00
source: pieces-ltm
pieces_ids:
- 8274dabd-1d3d-443c-9bff-853e39ca5360
tags:
- raw
- pieces
permalink: llmeon/raw/2026-05-29-pieces-git-tag-management
---

## Asset 1 (Pieces: 8274dabd-1d3d-443c-9bff-853e39ca5360)

**Captured:** 2026-05-29T10:28:32.073923Z

```
The user is asking about Git commands to:
1. Move a tag `sandbox-testing-1-latest-release` to a new location (after a branch merge)
2. Delete the old tag and add it to the latest commit
3. Also add a version tag `v1.8.65` to the latest commit

This is a Git commands question - it's technical knowledge I can answer directly from my training data. Let me provide the exact Git commands needed.

The workflow they're describing:
1. After merging the branch, they want to:
   - Delete the existing `sandbox-testing-1-latest-release` tag (locally and remotely)
   - Create a new `sandbox-testing-1-latest-release` tag on the latest commit (HEAD)
   - Create a `v1.8.65` tag on the latest commit (HEAD)
   - Push both tags

I need to provide commands for deleting the old tag both locally and on the remote, then creating the two new tags on HEAD and pushing them up.

For moving tags after a merge, I should consider whether to use force-move with `git tag -f` locally and then push with `--force` to update the remote tag, since ArgoCD will be polling for the new tag position.

The delete-and-recreate approach is cleaner if they want to avoid force pushes entirely. I should also mention that annotated tags are preferable for releases since they capture metadata like the tagger and timestamp, whereas lightweight tags are just pointers to commits.
```