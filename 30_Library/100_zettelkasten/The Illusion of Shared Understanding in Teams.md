---
aliases: [Semantic Diffusion, Semantic Diffusion Creates False Alignment]
conformant: true
contradicts: []
created: 2025-08-29T15:18:49+00:00
epistemic_status: medium
evidence_links: ["[[Evidence - Evans DDD Meanings of Words Are Slippery Because All Language Rests on a Model]]", "[[Evidence - Evans DDD Reference Domain Experts and Developers Use Different Languages in the Same Team]]"]
last_reviewed: ''
modified: 2026-09-26T08:45:38+00:00
non_conformance_reason: ""
permalink: llmeon/30-library/100-zettelkasten/the-illusion-of-shared-understanding-in-teams
proposition: Team members who share terminology often assume they share a mental model when their individual models differ, and the mismatch surfaces only during a crisis.
tags: [communication, teams, TheHuman/Cognition/mental-model]
title: The Illusion of Shared Understanding in Teams
type: claim
updated: null
---

## The Illusion of Shared Understanding in Teams

In a team, there is often an illusion that a single, shared mental model of a system exists. In reality, the "team model" is a fragile patchwork of each member's individual, differing, and often tacit models.

The illusion occurs when members of a team believe they are aligned on a concept because they use the same terminology, but their underlying individual mental models are actually different.

### Mechanism

We cognitively shortcut to assuming alignment because it is more efficient than constant verification. This false consensus persists until a crisis or complex failure, at which point the differing underlying models cause confusion, conflicting actions, and chaotic incident response.

This is caused by semantic diffusion (below) and by the fact that much of what each member knows is tacit (see [[Tacit vs Explicit Knowledge]]).

### Semantic Diffusion

Semantic diffusion occurs when a team uses the same vocabulary to describe different underlying concepts, creating a false sense of alignment.

For example, team members might all agree to add more "replicas," but one person's mental model is of Kubernetes ReplicaSets, another's is of a read-only database replica with replication lag, and a third's is of a simple backup copy. All parties agree on the term but have a completely different picture of the work, leading to integration failures and mismatched expectations.

### Example

A team can discuss the number "infinity" ($\infty$). One person may hold a flawed model of it as just a very large, specific number (a location). Another may hold the more correct model of it as a direction or process. They agree on the word but have a fundamental misalignment that will only surface during a crisis or deep technical discussion.

### Related

- [[Evidence - Evans DDD Reference Domain Experts and Developers Use Different Languages in the Same Team]]—_Evans on role-specific vocabularies inside one team._
- [[Evidence - Evans DDD Meanings of Words Are Slippery Because All Language Rests on a Model]]—_Evans on why the same word carries different models._
- [[Tacit vs Explicit Knowledge]]—_Explains why the differing models stay hidden: they live in the tacit layer._
- [[Flawed Mental Models Limit Mastery]]—_The "bug in the model" pattern (that note carries "Bug in the Model" as an alias); the flawed models that sit under the shared word._
- [[Claim - The true product of a software engineering team is shared understanding of the system]]—_Extends this: shared understanding is the product, and this note explains why it is hard to achieve._
- [[SoT - Communication & Misunderstanding (The Experiential Filter)]]—_The general theory: misunderstanding is the default and shared understanding means sufficient overlap. This note is its team-scale specialisation._

[extends:: [[SoT - Communication & Misunderstanding (The Experiential Filter)]], confidence=medium]

### Where It Applies in ProdOS

- [[Protocol - Context Injection]]—_The Ubiquitous Language block in its Domain Manifesto is the countermeasure for a human and an LLM using the same words with different models._
- [[Protocol - Diagnose an Agent Failure]]—_The `ambiguous-terminology` and `unclear-user-requirement` root-cause classes are this illusion between a person and an agent._
- [[SoT - Mental Models in Software Development]]—_The individual-scale account of the mental models that diverge across a team._
