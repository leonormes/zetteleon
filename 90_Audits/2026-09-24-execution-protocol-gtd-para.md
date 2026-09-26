---
created: 2026-09-24T00:00:00+00:00
modified: 2026-09-24T00:00:00+00:00
permalink: llmeon/90-audits/2026-09-24-execution-protocol-gtd-para
title: 2026-09-24-execution-protocol-gtd-para
type: note
---

## Value check and ProdOS linking — [[SoT - Execution Protocol (GTD & PARA)]] — 2026-09-24

> Method note: the 1MCP server was down for this run, so there was no semantic or graph-tool search. Duplicate and coverage checks were lexical (`rg`) plus file reads, and coverage claims are downgraded accordingly.

### Verdict: needed, and central

- It is the only note that defines **PARA Container vs GTD Project vs Task**, the outcome-naming rule, the five-stage checklist and the Project and Task Definition of Done. A lexical search for those terms found them elsewhere only in [[Habit 3 - Put First Things First]] (which cites this SoT), [[LLM GTD Context]] (a prompt) and a project overview note. None redefines them.
- **Grounded:** three claims `support` it ([[Any Desired Outcome Requiring More Than One Step Is a Project and Must Be Tracked]] (an axiom), [[Every Clarified Item Must Pass a Binary Actionability Test to Determine Its Categorical Flow]], [[Effective Productivity Comes From the Bottom Up]]). It is not in the audit's gap list.
- **Depended on:** Habit 3 depends on it (with Habit 4 and [[MOC - ProdOS]] downstream), [[Protocol - Weekly Command Centre]] `implements` it, and about 20 files link in, including [[MOC - Action Management]] and [[MOC - ProdOS]].
- **Not redundant with the kernel spec:** [[SoT - PRODOS Core Specification]] covers the 120-second MVA loop; this SoT covers the taxonomy and exit test.

### The gap

It had **no outbound links**, and three protocols that act on projects and tasks did not point to it: [[Protocol - Action-First GTD (LLM Chief of Staff)]], [[Protocol - Autonomous Action System]] and [[Protocol - Vague-to-Action]]. The kernel spec did not cite it from its Execution Protocols section.

### Changes

| File | Change |
|---|---|
| The SoT | new `## Where It Runs` section: 5 annotated links, each naming the stage it executes |
| Protocol - Action-First GTD | Related bullet plus `[implements:: [[SoT - Execution Protocol (GTD & PARA)]], confidence=medium]` |
| Protocol - Autonomous Action System | new `## Related` section plus the same `implements` edge |
| Protocol - Vague-to-Action | Related bullet (plain, no edge) |
| SoT - PRODOS Core Specification | one sentence under §3 pointing at the SoT |

**Why `implements` for two protocols and a plain link for the third:** Action-First GTD and the Autonomous Action System operate the SoT's stages directly (they sort into Project vs Next Action, and check project health). Vague-to-Action already `implements` the kernel spec and only borrows the naming and done rules, so it is linked plainly. `implements` is structural and does not change exposure. Weekly Command Centre already had its edge.

### Not done, and why

- **[[Operating Protocol for High-Friction Engineering Work]]** has an "H. Definition of Done" that echoes the Project DoD. It is a working note in `200_Projects`, not a protocol, so I did not link it.
- **[[Effective Productivity Comes From the Bottom Up]]** shows an untyped node (`[?]`) in the SoT's grounding tree. It is a foundation for the SoT and worth typing.
- **Tags:** the SoT carries `system/protocol` while its type is `sot`. Left alone.
- **Full-picture caveat:** the Weekly Command Centre runs only a reduced Reflect (Tier 0), whereas this SoT's Phase 4 asks for a full weekly scan of every Container. That is a deliberate reduction in that protocol, but the two do not describe the same review.

### Validation

Whole-vault `edge_lint.py`: `0 error(s), 0 warning(s)` (2839 notes, 1380 edges).
