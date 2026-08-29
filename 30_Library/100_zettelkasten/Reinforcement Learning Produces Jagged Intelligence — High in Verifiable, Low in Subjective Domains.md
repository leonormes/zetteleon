---
conformant: true
created: 2026-04-10T13:00:00+00:00
epistemic_status: high
modified: 2026-08-29T09:36:05+00:00
permalink: llmeon/30-library/100-zettelkasten/reinforcement-learning-produces-jagged-intelligence-high-in-verifiable-low-in-subjective-domains
prodos.kind: atomic
prodos.lifecycle: stable
proposition: Reinforcement Learning produces jagged intelligence, excelling in domains with verifiable success signals (like code) while stalling in subjective domains (like humor or writing).
tags: [constraints, intelligence, llm, reinforcement-learning]
title: Reinforcement Learning Produces Jagged Intelligence — High in Verifiable, Low in Subjective Domains
type: claim
---

%%[supports:: [[Agentic Autonomy Accelerates Fastest in Domains Where Success Is Verifiable]], strength=4, confidence=high]%%

## Reinforcement Learning Produces Jagged Intelligence—High in Verifiable, Low in Subjective Domains

Current AI models exhibit PhD-level competence in verifiable tasks (such as coding) alongside failure in subjective tasks (such as humour) because Reinforcement Learning can only effectively optimise against verifiable outputs. Where there is a clear success signal (code that runs, proof that holds), RL drives rapid capability improvement. Where no objective signal exists (is this joke funny?), RL stalls and the model's performance remains near its pre-training floor.

### Scope & Conditions

Applies to models trained with RL on feedback-heavy verifiable data. "Jagged" is a deliberate term—the capability profile is not uniformly high or uniformly low; it is highly domain-specific. High capability in one area does not predict capability in adjacent areas if those areas differ in verifiability.

### Evidence

> "This is attributed to the fact that reinforcement learning (RL) is effectively applied to verifiable outputs (code that runs) but remains stagnant in subjective areas (jokes), leading to highly specialised but uneven capabilities."

### Implications

- Model intelligence should not be treated as a single dimension; capability assessments must be domain-specific.
- Creating verifiability for currently subjective tasks is an active research lever for expanding RL's reach—e.g. converting "good writing" into a structured rubric with binary sub-criteria.

%%[supports:: [[AI and Machine Understanding]]]%%

%%[supports:: [[SoT - AI Sycophancy]]]%%

### Related

- [[AI and Machine Understanding]]—The jaggedness observation provides a mechanistic explanation for why AI cannot achieve unified understanding; the uneven capability profile is a direct consequence of RL's dependence on verifiable signals, not a temporary gap.
- [[SoT - AI Sycophancy]]—Sycophancy in subjective domains (feedback, creative tasks) is the specific failure mode that emerges when RL cannot optimise the dimension; the model defaults to approval-seeking precisely where it lacks a ground-truth signal.
