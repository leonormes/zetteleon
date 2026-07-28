---
title: The Vault's Primary Reader (Human vs Model) Is an Unstated Premise That Determines
  Every Design Decision Downstream
type: claim-stub
status: proposed
created: 2026-07-27 19:35:00+01:00
source_raw:
- - raw/proposed-claims/2026-07-27-vault-reader-tension
claim_statement: Every design decision in a PKM vault — note shape, linking strategy,
  prompt architecture, edge vocabulary — flows from an unstated answer to the question
  'who is the primary reader?' All four foundational PKM claims in the LLMeon vault
  assume different answers without acknowledging the divergence.
steel_man: 'A vault can serve both masters: writing proposition-centred notes for
  model retrieval while also maintaining personal-context connections for human sense-making.
  The two design goals are complementary, not conflicting — a well-structured note
  is good for both.'
tags:
- claim-stub
- agent-proposed
- vault
- pkm
- governance
falsifiers: null
crux: null
confidence: null
counter_positions: null
permalink: llmeon/raw/proposed-claims/2026-07-27-vault-reader-tension
---

This stub surfaces a tension that runs beneath four established claims in the LLMeon vault, none of which state their assumption about the vault's primary audience.

**PKM Generates Unique Insights via Personal Context That AI Cannot Replicate** assumes the human is the reader: the value is manual linking rooted in personal experience, which the task description explicitly says AI cannot replicate. The vault's purpose is subjective sense-making. [source: 30_Library/100_zettelkasten]

**Proposition-Centred Notes Make Superior RAG Chunks for LLM Context Engines** assumes the model is the reader: notes are evaluated by their semantic density as RAG chunks, MOC architecture supplies relational context for an LLM's retrieval, and the paradigm is "my AI assistant reasons with my notes as working memory."

**Local-First Obsidian with MCP and RAG Is the Best-Fit Substrate for Data-Sovereign PKM** assumes both: the vault serves human (data sovereignty, git workflows) and model (MCP/RAG integration). But "both" is not an adjudication — it defers the question of what happens when the two design goals pull in opposite directions (e.g. human-navigable prose vs structured claim chunks).

**PKM as Sense-Making Engine** assumes the human is the reader: PKM tracks the evolution of personal opinions, prioritises "why" behind beliefs, and the alternative ("static encyclopaedia") is explicitly rejected.

**Consequence for the P5 router:** A router that optimises for model-readability (structured claims, typed edges, proposition chunks) may produce notes that lose the personal-context thread that makes PKM valuable for the human. A router that preserves human sense-making may produce notes too discursive for reliable LLM retrieval. The router cannot be designed until this premise is stated.