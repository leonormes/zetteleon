---
title: A shared agent-skill specification makes the runtime swappable and relocates lock-in from the vendor to the skill library
type: claim-stub
status: proposed
created: 2026-07-27 17:36:00+01:00
source_raw: '[[raw/2026-07-27-makeuseof-agent-skill-portability]]'
claim_statement: Where competing agent runtimes implement a common skill specification, a skill authored once runs on all of them with only filesystem-wiring differences, which makes the runtime a commodity and relocates accumulated investment — and therefore lock-in — from the vendor to the user's own skill library.
steel_man: Specification conformance is claimed far more often than it is achieved. A skill is only as portable as the tool surface, permission model, context budget and failure semantics it assumes underneath, none of which the skill specification standardises. Portability that holds for a document-conversion skill with no external calls will not hold for anything orchestrating MCP servers or relying on a runtime's particular sub-agent behaviour, so the practical result is a portable subset and a long tail that silently isn't.
tags:
- claim-stub
- agent-proposed
- domain/llm
- topic/agent-skills
- topic/vendor-lock-in
permalink: llmeon/raw/proposed-claims/2026-07-27-skill-portability-makes-the-agent-runtime-swappable
---

## Supporting Context

The source states that skills following the common agent-skill specification run across Claude, OpenClaw and Hermes "with only minor wiring differences", such that one need only "dial the skill in one agent, and then it's available for use across all others" [source: raw/2026-07-27-makeuseof-agent-skill-portability]. The concrete instance given is Anthropic's `document-skills` set, installable in Claude Code via a plugin command or copied folder-for-folder into the Hermes or OpenClaw skills directories: "Since they follow the same agent skill specification, the logic just works, and all you have to do is adjust whatever file system or storage each runtime uses" [source: raw/2026-07-27-makeuseof-agent-skill-portability]. This is not covered by the vault's existing treatment of skills, which documents progressive disclosure, the Skill/MCP/Subagent distinction, the triggering problem and distribution patterns, but says nothing about cross-runtime portability (see [[SoT - AI Agent Skill Architecture]]) [inference]. **Trust caveat:** the source is a consumer-tech listicle and demonstrates portability only for Anthropic's own document skills; whether third-party skills port cleanly is asserted rather than evidenced [source: raw/2026-07-27-makeuseof-agent-skill-portability].

<!-- Intentionally left blank for human completion per AGENTS.md §2.4 -->
## Falsifiers

## Crux

## Confidence

## Counter Positions
