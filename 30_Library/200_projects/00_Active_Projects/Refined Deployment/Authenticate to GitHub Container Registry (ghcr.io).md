---
aliases: []
confidence: ""
created: 2025-10-24T10:24:04Z
epistemic: ""
last_reviewed: ""
modified: 2025-12-31T23:08:50+00:00
purpose: ""
review_interval: ""
see_also: []
source_of_truth: []
status: ""
tags: ["container"]
title: Authenticate to GitHub Container Registry (ghcr.io)
type: ""
uid: 
updated: 
version: ""
---

## Authenticate to GitHub Container Registry (ghcr.io)

### Commands to Authenticate Docker to ghcr.io

## Refresh GitHub CLI Token with read:packages Scope

```sh
gh auth refresh -h github.com -s read:packages
```

## Use the Token to Authenticate Docker

```sh
gh auth token | docker login ghcr.io -u leonormes --password-stdin
```

### Example: Pull a Private Image

```bash
docker pull ghcr.io/thehyve/fitfile_etl_container_mkuh:0.4.3-test
```
