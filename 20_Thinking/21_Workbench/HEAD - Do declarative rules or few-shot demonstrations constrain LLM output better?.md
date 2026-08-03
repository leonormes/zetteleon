---
title: HEAD - Do declarative rules or few-shot demonstrations constrain LLM output
  better?
type: question
tension: The vault has no recorded evidence comparing rules against demonstrations,
  yet two notes each assume a different winner.
candidate_answers:
- Declarative rules (domain manifesto)
- Few-shot demonstrations
- Rules for invariants, demonstrations for format
related_claims:
- '[[SoT - Context Engineering]]'
- '[[Prompt Architecture Levels]]'
sources:
- '[[SoT - Context Engineering]]'
- '[[Prompt Architecture Levels]]'
tags:
- state/thinking
- prodos/head
conformant: true
status: open
prodos:
  kind: head
  lifecycle: active
created: 2026-08-03 13:20:30+01:00
modified: 2026-08-03 13:20:30+01:00
permalink: llmeon/20-thinking/21-workbench/head-do-declarative-rules-or-few-shot-demonstrations-constrain-llm-output-better
AoL: System
closing_condition: true
---

## The Question

[[SoT - Context Engineering]] advocates stating the 'laws of the universe' — invariants, constraints, a domain manifesto — as declarative rules. [[Prompt Architecture Levels]] treats few-shot examples as a distinct architectural level. Which actually constrains LLM output more reliably, and under what conditions?

## Why It Matters

Every prompt in `10_System/prompts/` is built on an implicit answer to this. The Prompt Library Router's own maintenance rule §5 already bets on demonstrations — it says an example missing `conformant` reliably produces notes missing `conformant`, so LLMs pattern-match off the example rather than the prose. That is one data point for demonstrations, recorded but never generalised.

## What I Currently Think

The router's observation is the strongest evidence I own and it favours demonstrations for *format*. My lean is that they do different jobs: rules constrain *what is true* (invariants an example cannot enumerate), demonstrations constrain *what it looks like*. If that is right, the two notes are not in conflict at all and both need the scope sentence added.

## What Would Settle It

Run one controlled comparison on a real prompt in this vault — take a prompt that currently uses only rules, add a worked example, and measure conformance across ~10 generated notes. Record it as an `evidence` note. That is a half-day experiment, not a research programme.

## Sources

- [[SoT - Context Engineering]]
- [[Prompt Architecture Levels]]