---
created: 2026-04-10T13:00:00+00:00
modified: 2026-04-10T16:52:03+00:00
tags: [deployment, devops, docker, qdrant]
title: Qdrant Supports In-Memory, Disk, and Docker Deployment Modes
---

## Qdrant Supports In-Memory, Disk, and Docker Deployment Modes

Qdrant can be deployed in three modes depending on the stage of development: in-memory for ephemeral scripts and prototyping (no persistence, zero setup); local disk for development work requiring data persistence between runs; Docker for production-grade, scalable service deployment. The progression is a natural ramp from experimentation to production with no fundamental change in the client API.

### Scope & Conditions

All three modes use the same client interface, so moving between them requires only a configuration change. The in-memory mode is unsuitable for any production use—data is lost on process exit. Docker deployment follows standard containerisation patterns.

### Evidence

> "run in-memory for simple scripts, store data locally on your disk, or run as a scalable service via Docker [25:43]"

### Implications

- Low friction for local prototyping: the in-memory mode removes the cold-start barrier of setting up a service before the integration is proven.
- Standardised production path: Docker deployment aligns with existing container orchestration infrastructure.

### Related

- [[Ephemeral Agents and Environments in Terraform Cloud]]—shared mechanism: both distinguish ephemeral (in-memory / ephemeral agent) from persistent (disk / long-lived infrastructure) deployment contexts, and both treat ephemeral as the low-risk default for iteration.
