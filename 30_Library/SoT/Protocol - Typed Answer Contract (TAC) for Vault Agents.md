---
created: 2026-07-17T00:00:00+00:00
description: Universal output-discipline protocol for any ProdOS vault agent. Enforces stated confidence, cited evidence, and an explicit uncertainty flag on every response " — no unlabelled free prose. Reference this from any prompt's Output Contract callout;" route here for the enforcement rule, and to SoT - Typed Answer Contract (TAC) for LLM Output for the underlying theory.
modified: 2026-08-13T10:53:39+00:00
permalink: llmeon/30-library/so-t/protocol-typed-answer-contract-tac-for-vault-agents
see_also: ["[[Goal - Orphan Triage Sweep (Daily Cron)]]", "[[SoT - Typed Answer Contract (TAC) for LLM Output]]"]
source_of_truth: true
tags: [domain/ai, sot, type/protocol]
title: Protocol - Typed Answer Contract (TAC) for Vault Agents
type: protocol
---

%%[implements:: [[SoT - Typed Answer Contract (TAC) for LLM Output]], strength=5, confidence=high]%%

> Output Contract: this note IS the Output Contract. It defines the rule other prompts point to—it has no upstream contract to follow, only the rules below.

## Purpose

Every ProdOS vault agent (persona, system, protocol, or goal prompt) must stop returning unstructured free prose as its final answer. This protocol adapts the Typed Answer Contract (TAC) pattern—normally enforced with a Pydantic/JSON schema in code—into a markdown-native rule set any LLM agent operating over this vault must follow, whether it is producing a chat reply, a new note, or an edit to an existing note.

Deep-dive theory, caveats, and the original schema this protocol is adapted from: [[SoT - Typed Answer Contract (TAC) for LLM Output]].

## The Rule Set

Any vault agent governed by this protocol (i.e. any prompt with an `> Output Contract:` callout pointing here) must apply all four rules below to its output:

1. State confidence. Every substantive claim or recommendation carries an explicit confidence signal—`high`, `medium`, or `low`—either inline (`(confidence: high)`) or as a short confidence line at the end of a section. Do not present speculative or inferred content with the same weight as directly-sourced content.
2. Cite evidence. Every factual claim about the vault's own content must point to its source: a `[[wikilink]]` to the specific note, and where practical, the quoted line or heading that supports the claim. Do not assert what a note says without linking to it. If synthesizing across many notes (e.g. Chronos-style synthesis), list the source notes actually used.
3. Flag insufficient context explicitly—never guess silently. If retrieval, search, or the note content genuinely does not contain enough information to answer, do not produce a plausible-sounding but unsupported answer. Say so directly, using the vault's existing `UNSURE` category (see [[Goal - Orphan Triage Sweep (Daily Cron)]]) as the model: state what's missing and propose the smallest next action to resolve it (e.g. "propose only—needs human confirmation"), rather than fabricating a placement, link, or fact.
4. Never blend outside knowledge with vault-retrieved facts unlabelled. When an agent's answer mixes general/training knowledge (e.g. "GTD methodology generally recommends…") with vault-specific facts (e.g. "your note says…"), the two must be visibly distinguished—through separate sections, inline attribution, or explicit phrasing ("in general," vs "in your vault,"). Do not let outside knowledge silently masquerade as a vault-sourced fact.

## Why This Exists

Free-text LLM output over a personal vault has the same failure mode as free-text RAG in production systems: confident-sounding but ungrounded prose is indistinguishable from grounded prose until a human catches the error—often too late, after a bad placement, a fabricated link, or an unsupported synthesis has already been written to a note. Structural rules that force confidence, evidence, and an uncertainty escape hatch catch these failures at generation time rather than relying on review discipline alone. See [[MVC Enforcement Structural Gates for LLM Agents]] for the same "structure over discipline" principle applied to context management.

## Scope

This protocol governs _output discipline_—how an agent presents what it produces. It does not replace or duplicate a prompt's own domain-specific rules (e.g. the Zettelkasten atomicity rules in [[Atomic Signal Extractor → Write TMP file]], or the GTD context rules in [[Optimised GTD Context Auditor for Pieces LTM]]). Apply TAC on top of, not instead of, each prompt's existing instructions.

## Maintenance Rule

Any new `type/system`, `type/protocol`, or `type/task-log`-adjacent prompt added to `10_System/prompts/` that produces vault content or user-facing analysis must include an `> Output Contract: follow [[Protocol - Typed Answer Contract (TAC) for Vault Agents]]` callout near its opening heading. See `00 - Prompt Library Router` for the full library-maintenance rules.
