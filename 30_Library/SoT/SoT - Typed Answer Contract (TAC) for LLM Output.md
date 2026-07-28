---
aliases: [Structured Output Contract, TAC, Typed Answer Contract]
created: 2026-07-17T00:00:00+00:00
modified: 2026-07-20T16:33:41+00:00
permalink: llmeon/30-library/so-t/so-t-typed-answer-contract-tac-for-llm-output
see_also: ["[[MOC - AI Software Engineering]]", "[[MVC Enforcement Structural Gates for LLM Agents]]", "[[SoT - Agentic AI Design Patterns]]", "[[SoT - AI Agent Skill Architecture]]", "[[SoT - PRODOS Core Specification]]"]
tags: [domain/ai, prodos/sot, topic/pkm]
title: SoT - Typed Answer Contract (TAC) for LLM Output
type: sot
---

%%[implements:: [[SoT - Flow Engineering]], strength=4, confidence=high]%%

## Minimum Viable Understanding (MVU)

An LLM should never return free-form prose as its final answer when the answer needs to be trusted, checked, or acted on. Force the output into a small structured contract instead—a schema with fields for the answer, a confidence score, source references, and an explicit "I don't have enough information" flag—and reject or hold back any output that fails to fill it in honestly. In production RAG systems this is enforced with a Pydantic/JSON schema and a validating library (`instructor`); in the ProdOS vault it is enforced with a markdown-native rule set (see [[Protocol - Typed Answer Contract (TAC) for Vault Agents]]). Either way, the mechanism is the same: structure forces honesty about what the model actually knows, catching hallucination _before_ it reaches the user rather than relying on the user to catch it after the fact.

## Working Knowledge (Core Concepts)

The Typed Answer Contract pattern, as described in the source article ("Stop Returning Text from RAG: The Typed Answer Contract That Prevents Hallucination," TDS, July 2026), replaces a RAG system's free-text response with a validated schema containing:

- `answer`—the actual response content.
- `is_definitive`—whether the model believes this fully answers the question, as opposed to a partial or hedged answer.
- `confidence`—a 0–1 self-assessed score for how well-supported the answer is by retrieved context.
- `source_ids`—explicit references to which retrieved chunks/documents were actually used, enabling traceability.
- `missing_info`—a boolean flag: if true, the answer is _never surfaced to the user_—the system instead reports that it cannot answer, rather than guessing.
- `evidence` (in extraction variants)—sub-fields like `source_quote` and `page_number`, forcing the model to point to the exact text it drew from rather than paraphrasing from memory.

The schema is validated and auto-retried (via `instructor` or an equivalent structured-output library) until the model actually produces a conformant object—the model cannot escape into unstructured prose. Reported production result (legal Q&A system): hallucination rate fell from 12% to 1.7%, with roughly 30% of generated answers rejected by the `missing_info`/low-confidence gate before ever reaching a user.

This is a specific, code-enforced instance of a more general principle already present in this vault: that reliability comes from structural gates, not from asking a model nicely to be careful. See [[MVC Enforcement Structural Gates for LLM Agents]] for the same idea applied to context assembly rather than output formatting.

## Current Understanding (Workflows & Practices)

In a code/production context (e.g. a FastAPI RAG backend), TAC is implemented literally: a Pydantic model, an `instructor`-wrapped LLM client, and application logic that branches on `missing_info` and `confidence` before ever rendering a response to a user.

In the ProdOS vault—a markdown/Obsidian agent context rather than a code pipeline—there is no schema validator sitting between the model and the note. The adaptation implemented here (2026-07-17) is a markdown-native version of the same contract, enforced by convention rather than by a validator:

- Every governed vault-agent prompt (persona/system/protocol prompts in `10_System/prompts/`) carries an `> Output Contract:` callout pointing at [[Protocol - Typed Answer Contract (TAC) for Vault Agents]].
- That protocol requires: stated confidence (`high`/`medium`/`low`), cited evidence (`[[wikilink]]` + quoted line where practical), an explicit "insufficient context" flag instead of a guessed answer, and clear separation between outside/training knowledge and vault-retrieved facts.
- The vault already had a working instance of the `missing_info` idea before TAC was named as such: [[Goal - Orphan Triage Sweep (Daily Cron)]]'s `UNSURE` category, where the daily orphan-repair sweep proposes placements only, and explicitly flags notes it can't confidently place rather than forcing a guess. TAC formalizes and generalizes that existing pattern across the whole prompt library rather than introducing a new one.
- This is intentionally a lighter-weight enforcement than the code version: there is no automatic rejection/retry loop, so the contract depends on each prompt actually following its Output Contract callout—a discipline-plus-structure hybrid rather than a pure structural gate. Reviewer note: reintroducing an actual programmatic check (e.g. a linter that verifies agent output has the four required elements) would close this gap if unreliability becomes visible in practice.

Related implementation touchpoints:

- [[SoT - Agentic AI Design Patterns]] §2E (Knowledge Retrieval/RAG) and §3 (Implementation in ProdOS, "Reliability") now reference this SoT.
- [[MOC - AI Software Engineering]] §8 indexes this as a peer to the vault's other AI-engineering patterns (Cognitive Bridge, Context Rot, LLM Wiki Pattern, etc.).
- [[SoT - AI Agent Skill Architecture]]'s progressive-disclosure principle is complementary: TAC governs _what shape the output takes_, skill architecture governs _what context the agent has access to_ when producing it.

## Tensions & Gaps

- Schema complexity trade-off. The source article notes schemas with 15+ nested fields start to _degrade_ model performance rather than improve reliability—there's a real ceiling on how much structure helps. The markdown adaptation here deliberately stays to four rules, not an exhaustive field list, for the same reason.
- Self-assessed confidence can be overconfident. A model scoring its own `confidence` field is still the same model that might hallucinate the answer—self-assessment is a useful signal, not a guarantee. Treat stated confidence as a prioritization aid for human review, not proof of correctness.
- Structure doesn't fix broken retrieval. TAC (in either its coded or markdown form) makes it _visible_ when an agent lacks sufficient grounding—it does not improve the underlying retrieval/search quality. If a vault agent's source notes or search results are themselves incomplete or poorly indexed, TAC will more reliably surface an `UNSURE`/low-confidence result, but it cannot manufacture correct answers from bad retrieval.
- No automated enforcement yet. As noted above, the vault-native version relies on each governed prompt's own compliance with its Output Contract callout; nothing currently checks vault-agent output post-hoc against the four rules. This is a known gap, not a design choice—worth revisiting if agent output drifts from the contract in practice.
- Origin note superseded. This SoT supersedes the working note `Typed-Answer-Contract-RAG.md` (formerly in `20_Thinking/21_Workbench/`), which has since been moved to `.trash/` now that its ideas are embedded here and in the governed prompts.
