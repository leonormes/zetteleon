---
aliases: [Output Contract, Protocol - Typed Answer Contract, Structured Output Contract, TAC, Typed Answer Contract, Vault Agent Output Contract]
conformant: true
contrasts_with: ["[[SoT - Context Rot]]"]
created: 2026-07-17T00:00:00+00:00
modified: 2026-11-14T17:08:14+00:00
permalink: llmeon/30-library/so-t/so-t-typed-answer-contract-tac-for-llm-output
project_category: prodos
see_also: ["[[Goal - Orphan Triage Sweep (Daily Cron)]]", "[[SoT - Agentic AI Design Patterns]]", "[[SoT - AI Agent Skill Architecture]]", "[[SoT - Knowledge Compiler (Argument Graph Spec)]]"]
status: stable
tags: [domain/ai, prodos/sot, sot, topic/pkm, type/protocol]
title: SoT - Typed Answer Contract (TAC) for LLM Output
type: sot
upstream: ["[[SoT - Flow Engineering]]", "[[SoT - PRODOS Core Specification]]"]
---

> Canonical status: this note is the unified Source of Truth and enforcement protocol for the Typed Answer Contract (TAC) across both production LLM pipelines and ProdOS vault agents.

## Minimum Viable Understanding (MVU)

An LLM must never return ungrounded free-form prose when its output needs to be trusted, checked, or written to the vault. Fluent prose masks hallucination behind the illusion of substance ([[Felt significance of thoughts can mislead about their substance]]). Force the output into a small Typed Answer Contract (TAC) instead: explicit confidence, traceable source citations, a mandatory `missing_info` / `UNSURE` escape hatch, and hard structural validation gates before any file mutation is accepted. In code RAG systems this is enforced via Pydantic/`instructor`; in the ProdOS vault it is enforced via a Two-Tier Gate (`AGENTS.md` §7 + executable CLI validators).

---

## 1. The Vault Agent Output Contract (The 4 Mandatory Rules)

Every ProdOS vault agent or prompt (including any prompt carrying an `> Output Contract:` callout) must apply all four rules below:

1. State Confidence (`high` | `medium` | `low`): Every substantive claim, classification, or recommendation carries an explicit confidence signal—inline (`(confidence: high)`) or at section end. Never present inferred or speculative claims with the same weight as directly verified vault facts. Treat self-assessed confidence as a human-review prioritisation aid, not proof of correctness.
2. Cite Vault Evidence (`[[wikilink]]`): Every factual claim about the vault's content must point to its exact source note (`[[Note Title]]`) and, where practical, the section or quoted line. Never assert what a note says or whether a note exists without reading/searching first.
3. Flag Insufficient Context Explicitly (`UNSURE`): If search, retrieval, or note text does not contain enough evidence to answer or wire an edge, halt and output `UNSURE` (modelled on [[Goal - Orphan Triage Sweep (Daily Cron)]]). State what is missing and propose the smallest safe next step (e.g. a stub in `00_Inbox/` or a human decision) rather than guessing or fabricating links, titles, or facts. If you fell back from 1MCP/CLI to lexical search, declare your tooling tier and downgrade coverage claims.
4. Separate Vault Facts from Outside Knowledge: Never blend general model training knowledge with vault-retrieved facts unlabelled. Distinguish them explicitly via separate headings or inline attribution (_"In general…"_ vs. _"In `[[Note]]`…"_).

---

## 2. Production RAG Architecture & Theoretical Grounding

In production RAG systems ("Stop Returning Text from RAG: The Typed Answer Contract That Prevents Hallucination," July 2026), free-text generation is replaced by a validated schema (`instructor` / Pydantic) containing:

- `answer`: the response content.
- `is_definitive`: boolean indicating whether retrieved context fully answers the query.
- `confidence`: `0.0–1.0` support score against retrieved chunks.
- `source_ids`: explicit chunk/document identifiers used.
- `missing_info`: boolean gate—if `true`, the system suppresses the generated answer and reports what cannot be verified instead of guessing.
- `evidence`: structured `source_quote` and location fields forcing exact grounding rather than memory paraphrase.

Empirical Impact & Schema-Complexity Ceiling:

- Hallucination Drop: Validation + auto-retry reduced production legal Q&A hallucinations from 12% to 1.7%, with ~30% of ungrounded answers intercepted by the `missing_info` / low-confidence gate before reaching a user.
- The ~15-Field Ceiling: Schemas exceeding ~15 nested fields degrade LLM reasoning and compliance. ProdOS enforces this ceiling across the stack: 4 rules for agent output (§1), minimal YAML envelopes in [[SoT - ProdOS Frontmatter Contract (Note Type Schemas)]], and 7 closed predicates + 2 optional attributes (`strength`, `confidence`) in [[SoT - Typed Edge Vocabulary (Knowledge Graph Relations)]].

---

## 3. Two-Tier Enforcement in ProdOS (Structure Over Discipline)

An earlier version of this spec relied solely on prompt callouts ("enforced by convention rather than by a validator"). ProdOS now enforces TAC through a Two-Tier Structural Gate codified in `AGENTS.md` §7:

| Tier | Scope | Enforcement Mechanism | Failure Handling |
|:--- |:--- |:--- |:--- |
| Tier 1: Epistemic Output Gate | Chat replies, triage tables, audit reports, synthesis proposals | `AGENTS.md` §7.1 + `> Output Contract:` callouts across `10_System/prompts/` enforcing Rules 1–4 (`confidence`, `[[wikilink]]`, `UNSURE`, source separation). | Classified as `tac-or-output-validation-failure` under [[Protocol - Diagnose an Agent Failure]]; requires a root-cause fix + regression case in `10_System/evals/`. |
| Tier 2: Pre-Completion Write Gate | Creating, editing, or wiring any note in the vault | Mandatory CLI validators (`AGENTS.md` §7.2) that exit non-zero on schema, shape, or graph violations before `shale done`. | Agent must fix all errors (`0 error(s)`) or set `conformant: false` with an explicit `non_conformance_reason` rather than faking compliance. |

### Tier 2 Executable Validators (Mandatory Before `shale done`)

1. Frontmatter Contract Gate (`validate_note_frontmatter.py`):

   ```bash
   uv run --with pyyaml python3 10_System/scripts/validate_note_frontmatter.py --path "<file>"
   ```

   Verifies `title`, `type`, `tags`, `conformant`, `status`, and `type`-specific fields (`proposition`, `epistemic_status`, `contradicts`, `evidence_links` on claims) per [[SoT - ProdOS Frontmatter Contract (Note Type Schemas)]]. If an agent cannot verify a required field, it must set `conformant: false` and populate `non_conformance_reason` (the note-level equivalent of `missing_info: true`).

2. Atomic Proposition Gate (`validate_note_shape.py`):

   ```bash
   python3 10_System/scripts/validate_note_shape.py "<file>"
   ```

   Enforces [[SoT - Atomic Note Standard (The Proposition Card)]] on atomic notes created in `30_Library/100_zettelkasten/`.

3. Knowledge Compiler & Edge Gate (`edge_lint.py`):

   ```bash
   uv run --with pyyaml python3 10_System/scripts/edge_lint.py
   ```

   Enforces [[SoT - Typed Edge Vocabulary (Knowledge Graph Relations)]] and [[SoT - Knowledge Compiler (Argument Graph Spec)]]: rejects unknown predicates, bare note targets, dangling links, and ambiguous targets (`0 error(s)` required), while `--audit` checks C1–C3 argument grounding.

4. Protected-Note & Provenance Gate (`AGENTS.md` §6 & `shale`):
   Agents never edit notes with `own_words: true` or existing notes in `01_journals/` and `20_Thinking/`, and bracket every file-editing task with `shale intent` and `shale done`.

---

## 4. Known Limits & Guardrails

- Self-Assessed Confidence Is Not Grounding: A model scoring its own `confidence` is vulnerable to the same fluency bias it is rating ([[Felt significance of thoughts can mislead about their substance]], [[SoT - Illusion of Explanatory Depth (IoED)]]). Confidence orders human review; `[[wikilink]]` evidence and `edge_lint.py` verify the facts.
- Structure Cannot Fix Blind Retrieval: TAC makes missing context _visible_ (`UNSURE` / `conformant: false`), but cannot manufacture knowledge from incomplete search. Always prefer Tier 1 `obsidian-llmeon` 1MCP semantic/text tools + `obsidian` CLI over raw filesystem grep (`AGENTS.md` §9.1).

---

## 5. Related Architecture & Epistemic Claims

- [[SoT - PRODOS Core Specification]]—_Implements Phase 2 Refinement & Architect Mode agent governance._ [implements:: [[SoT - PRODOS Core Specification]], strength=5, confidence=high]
- [[SoT - Flow Engineering]]—_Replaces prompt-level wishful thinking with structural validation gates._ [implements:: [[SoT - Flow Engineering]], strength=4, confidence=high]
- [[MVC Enforcement Structural Gates for LLM Agents]]—_Synthesises the structural-gate principle: MVC gates what context enters the agent, TAC gates what output and writes leave it._ [synthesizes:: [[MVC Enforcement Structural Gates for LLM Agents]], strength=4, confidence=high]
- [[Protocol - Diagnose an Agent Failure]]—_Defines the `tac-or-output-validation-failure` root-cause class and `10_System/evals/` regression requirement._ [supports:: [[Protocol - Diagnose an Agent Failure]], strength=4, confidence=high]
- [[SoT - Context Engineering]]—_Upstream context-compression discipline paired with TAC output discipline._
- [[Felt significance of thoughts can mislead about their substance]]—_Cognitive basis for why fluent, confident-sounding LLM prose requires explicit evidence and uncertainty gates._
