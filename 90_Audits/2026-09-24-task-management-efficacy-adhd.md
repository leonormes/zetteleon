---
created: 2026-09-24T00:00:00+00:00
modified: 2026-09-24T00:00:00+00:00
permalink: llmeon/90-audits/2026-09-24-task-management-efficacy-adhd
title: 2026-09-24-task-management-efficacy-adhd
type: note
---

## Broken links, value check and ProdOS linking — [[Task Management Systems Have Limited Efficacy for ADHD Productivity]] — 2026-09-24

> Method note: 1MCP tools were unavailable, so checks were lexical (`rg`) plus file reads, a filename-and-alias resolver script, and `edge_lint.py`.

### Broken link: 1 found, fixed

`source: '[[MOC - ADHD Task Management]]'` pointed at a MoC that does not exist (no file, no alias). Retargeted to [[MOC - Action Management]], the hub that "aggregates the principles, systems, and strategies for managing action" and is built to counter ADHD task-initiation deficits. The note is now also listed there. After the edit a resolver run finds **0 unresolved links**.

### Verdict: keep

- **Useful:** it states the honest limit of ProdOS's own task machinery (GTD, Todoist, the Chief of Staff): a system only captures and organises; starting is the ADHD bottleneck. That is the premise behind [[Protocol - Vague-to-Action]] and the starter-task notes.
- **Well grounded once linked:** its premise [[ADHD Task Initiation Difficulty is a Neurological Issue Not Laziness]] rests on [[SoT - The Interest-Based Nervous System in ADHD]] and a dopamine hyposensitivity claim, and bottoms out on evidence including a Volkow 2009 PET study. The audit does not flag the note.
- **Short and single-idea (142 words):** nothing to atomise.

### Changes

| File | Change |
|---|---|
| The note | `source` fixed; `proposition`, `epistemic_status: medium`, `evidence_links` (the striatal-dopamine Evidence note), empty `contradicts`, `conformant: true`; `[depends_on:: [[ADHD Task Initiation Difficulty is a Neurological Issue Not Laziness]], confidence=medium]`; `## Related` (6 links) and `### Where It Applies in ProdOS` (5 links) |
| MOC - Action Management | one bullet under Core Architecture |

**Why `depends_on`:** the claim fails if initiation is not the main bottleneck, so the premise is genuinely load-bearing. The premise is itself grounded, so this adds no ungrounded foundation. **Why the evidence link is scoped:** the striatal evidence supports that initiation is the harder problem, not that task systems are ineffective, and the Related bullet says so.

### ProdOS linking

[[SoT - Execution Protocol (GTD & PARA)]] (the system in question), [[Protocol - Vague-to-Action]] and [[The Three Rules of Starter Tasks]] (the initiation answers), [[SoT - Prosthetic Executive Function]] and [[SoT - Bridging the Intention-Action Gap]].

### Left alone

- **The same dangling source** `[[MOC - ADHD Task Management]]` appears in three other notes: [[Interest Pairing Can Increase Engagement in Mundane Tasks for ADHD]], [[Designed Task Switching Leverages Dopamine Boosts for ADHD Motivation]] and [[Reframing Language from Obligation to Purpose Boosts ADHD Task Initiation]]. It looks like a renamed or removed MoC. The same retarget would fit, but they are out of scope for this run.
- **Sibling note:** [[ADHD Brain Wiring vs. Classic Productivity Systems]] is the wider argument; it was fixed in the previous run.

### Validation

Whole-vault `edge_lint.py`: `0 error(s), 0 warning(s)` (2858 notes, 1383 edges).

---

## Follow-up — dangling MoC retargeted in the other notes

Leon approved applying the same retarget. `[[MOC - ADHD Task Management]]` was a live link in **two** notes, not three: [[Designed Task Switching Leverages Dopamine Boosts for ADHD Motivation]] and [[Reframing Language from Obligation to Purpose Boosts ADHD Task Initiation]] now have `source: '[[MOC - Action Management]]'`. [[Interest Pairing Can Increase Engagement in Mundane Tasks for ADHD]] had already been repaired earlier (its `source` is [[MOC - ADHD Experiments & Protocols]]); it only mentions the old name in prose explaining that repair, which is not a link, so I did not touch it. My earlier "three notes" count was a text match, not a link check.

No `[[MOC - ADHD Task Management]]` link remains anywhere in `30_Library` or `10_System`.

**A choice to revisit:** the Interest Pairing repair used the Experiments hub, which fits because all three are `type: hypothesis` experiments. The two notes above are also hypotheses, so [[MOC - ADHD Experiments & Protocols]] would arguably fit them better than Action Management. I followed the instruction as given.

Validation: whole-vault `edge_lint.py` `0 error(s), 0 warning(s)`.
