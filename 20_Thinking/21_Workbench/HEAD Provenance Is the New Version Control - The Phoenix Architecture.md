---
captured: 2026-06-17T10:35:49+01:00 2026-06-17T10:35:49+01:00
created: 2026-06-17 09:35:51+00:00
modified: 2026-06-17 09:39:48+00:00
source: https://aicoding.leaflet.pub/3mcbiyal7jc2y
status: processing
tags:
- input
title: HEAD Provenance Is the New Version Control - The Phoenix Architecture
type: head
permalink: llmeon/20-thinking/21-workbench/head-provenance-is-the-new-version-control-the-phoenix-architecture
---

## Raw Output / Content

When code can be thrown away and recreated, the unit of change is no longer lines of code. It's reasons. Version control has to follow.

Regenerable systems quietly invalidate an assumption that has underpinned software engineering for decades: that the text of the code is the best record of how and why a system came to be. Once an AI can reliably regenerate an implementation from specification, the code itself becomes an artifact of synthesis, not the locus of intent.

By regenerable, I mean: if you delete a component, you can recreate it from stored intent (requirements, constraints, and decisions) with the same behavior and integration guarantees.

In that world, version control doesn't disappear, but it has to move upstream.

## When Diffs Stop Representing Decisions

Traditional version control works because code edits are a reasonable proxy for human decisions. Someone typed this conditional. Someone refactored that loop. A diff is an imperfect but serviceable record of authorship.

AI-assisted generation severs that link.

When an agent reads a specification, reasons about constraints, chooses an approach, and emits code, the resulting text reflects outcomes, not decisions. A diff can show what changed in the artifact, but it cannot explain which requirement demanded the change, which constraint shaped it, or which tradeoff caused one structure to be chosen over another.

This is the sense in which code-first version control becomes a lossy history. Not because diffs are useless (they still matter operationally) but because they no longer represent the causal history of the system. They tell you what happened, not why it happened.

That distinction matters once code is no longer directly authored.

## Specifications as Executable Intent

In a regenerable system, specifications are no longer descriptive documents. They are executable inputs.

If a component can be deleted and recreated at will, then whatever information is required to recreate it is, by definition, the source of truth. Specifications stop being explanatory prose and become causal inputs.

The same is true of an agent's plan.

The plan that matters isn't free-form thinking. It's the decision record: chosen strategy, rejected alternatives, and the constraints that forced the choice. Even when the choice is wrong, it's still the most useful artifact to preserve: it explains why the system looks like this. Treating this as throwaway reasoning discards information that is often more important than the final text.

The plan is not documentation. It is part of the implementation.

## A Concrete Example: Email Validation

Consider a small component: a function that validates email addresses.

A specification might state:

> The system must accept standard email addresses of the form `local@domain`.

> It must reject inputs without exactly one `@`.

> It must not attempt full RFC compliance.

An agent produces a plan:

> Use a simple regular expression.

> Do not rely on external libraries.

> Explicitly reject whitespace.

> Favor readability over completeness.

From this, code is generated.

Now the requirement changes:

> The system must accept internationalized domain names (IDN) in the domain portion.

Nothing else changes.

![](https://aicoding.leaflet.pub/api/atproto_images?did=did:plc:4qsyxmnsblo4luuycm3572bq&cid=bafkreielarcqw4dte7egyhiuighu3d4wtynsonruh6dqmluhvmdubexejm&v=1)

In a code-centric workflow, you inspect the diff and infer intent after the fact. In an intent-centric workflow, a single requirement node changes, the dependent plan node(s) changes, and the generated code changes as a consequence. The unit of change is not "these lines," but "this reason."

You can now answer not just what changed, but why it had to.

## From Files to Intent Graphs

To support this, intent cannot live in a loose collection of documents. It needs structure.

The representation that works is a [content-addressed](https://en.wikipedia.org/wiki/Content-addressable_storage) graph. Individual requirements, constraints, plans, decisions, and environmental factors become nodes. Each node has a stable representation and a hash derived from its content. Edges express causality: this plan depends on that requirement; this decision exists because of that constraint.

In practice, each node needs at least: a type, canonical content, explicit dependencies, and evaluation artifacts (tests, constraints, budgets) that make regeneration checkable.

Even in the small example above, the graph is explicit:

- A requirement node: "accept standard email addresses"
- A constraint node: "no RFC compliance"
- A plan node: "use a regex, reject whitespace"
- A generator node: "Claude-class model, email-validator template"

The code sits downstream of all four.

The "version" of the component is the root hash of this graph. Change a requirement and only the downstream nodes change. Regenerate with identical inputs and the root hash remains stable. Identity moves from files to intent.

## What's New and What Isn't

None of these ideas exist in isolation.

Build systems like [Bazel](https://bazel.build/)—and increasingly [Nix](https://nixos.org/) -style systems—use hashed inputs and content-addressed caches to track which inputs produced which outputs. Formal methods [have long pursued](https://lamport.azurewebsites.net/pubs/lamport-ftrtft94.pdf) specifications with mathematical semantics precise enough to analyze and verify.

What's new is the coupling.

Bazel tracks build causality. Formal specifications describe logical intent. Regenerable systems require generative provenance: a direct, machine-enforced link between intent and implementation. The specification graph doesn't sit beside the system. It drives it.

Description can drift. Drivers cannot.

## Why Traceability Failed and Why It Might Not Now

Industries have attempted requirements traceability for decades, usually through tickets, spreadsheets, and process checklists. It often failed in mainstream software because humans were asked to maintain links that the system itself did not depend on.

Regenerable systems invert the incentives.

If a system can regenerate itself, it must already know what it's doing. Provenance stops being overhead and becomes infrastructure. The links exist because generation requires them.

This does not describe how today's AI tools work. Current generators do not emit stable, versionable plans or structured intent graphs. This is not a description of the present. It's an argument about the direction forced by regeneration economics: the cost of re-deriving code keeps falling, while the cost of rediscovering intent does not.

## Hard Problems and Failure Modes

This model raises real challenges.

Specifications expressed in natural language require canonicalization. Two nodes may be semantically equivalent but textually different, and we won't always detect that reliably. Agents will make implicit assumptions that are not explicitly recorded. Non-deterministic generators may produce different code from identical intent graphs.

These are not reasons to abandon the approach. They are design constraints.

The model does not require perfect formalization. It requires tractability—and tractability improves as specifications become more structured, plans become explicit, and generators are forced to surface their decisions. Ambiguity becomes visible rather than hidden in diffs.

Even failure becomes diagnosable at the level that matters: intent.

## Versioning What Actually Matters

Git taught us how to version text.

Regenerable systems force us to version intent: the requirements, constraints, and decisions that caused a system to take its current shape. Code still matters but it becomes an artifact, not the record of authorship.

The tools to do this well don't fully exist yet. But the pressure is already here. If code can be recreated at will, the question becomes unavoidable:

What, exactly, is worth preserving, and how would you know?

### The Phoenix Architecture

Generative AI coding demands what we've always known: modularity, clear boundaries, disposable components. Principles that scaled human teams are now table stakes. Here, we make the implicit explicit