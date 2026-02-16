---
created: 2026-02-14T09:01:46+00:00
modified: 2026-02-15T10:20:41+00:00
title: Two note types, one linking convention
---

Right, Leon—this is a cracking problem to solve. Context Rot is essentially a cache-miss in your personal knowledge base, and the fix is to treat your notes like infrastructure: typed, tagged, and composable.

Let me build you the template system and an example playbook so you can see it working end-to-end.Now let me create a concrete example of each so you can see the system working, not just the skeleton.Here's the system—two templates and two worked examples. Let me walk you through the design decisions so you can judge whether they fit your brain:

## The Architecture

Two note types, one linking convention:

- Atomic Command (`tag: cmd`) One command, one purpose, one execution context. The unit of reuse.
- Playbook (`tag: playbook`)—A directed graph of Atomic Commands linked with `[[wikilinks]]`. The unit of workflow.

Playbooks never contain raw commands inline. They only _point to_ Atomic Commands. This means when `kubectl` syntax changes or you discover a better flag, you update one note and every playbook that references it inherits the fix.

## Why These Properties Matter

The YAML frontmatter is doing the heavy lifting for discoverability:

- `hop_level` solves the "wait, where do I run this?" problem. Every command declares its execution context, and the Prerequisites table links to the tunnel/auth commands you need to get there. No more running a `kubectl` command locally and wondering why it times out.
- `tool` lets you use Obsidian Dataview queries like `TABLE FROM #cmd WHERE tool = "argocd"` to generate dynamic indexes without maintaining folder structures.
- `status` + `last_verified` gives you confidence scoring. If `last_verified` is 6 months old, you know to double-check before trusting it during an incident.

## The Verification Principle

Every Atomic Command has a Failure Signature callout. This is the key anti-Context-Rot mechanism—it's not enough to know the command, you need to know what _bad_ looks like so you can branch to the right next step without Googling.

## Your Immediate Next Action

1. Create a folder in your Obsidian vault called `ops/` (flat—no subfolders)
2. Drop both templates into `ops/` as `_atomic-command-template.md` and `_playbook-template.md` (the underscore keeps them sorted to the top)
3. Drop the two examples into `ops/` alongside them
4. Pick one command you ran this week that you had to look up—create an Atomic Command note for it using the template

That fourth step is the seed. Once you've got 5–6 atomic commands, the playbooks practically write themselves because the linking structure makes the gaps obvious.
