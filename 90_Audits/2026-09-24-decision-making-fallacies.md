---
created: 2026-09-24T00:00:00+00:00
modified: 2026-09-24T00:00:00+00:00
permalink: llmeon/90-audits/2026-09-24-decision-making-fallacies
title: 2026-09-24-decision-making-fallacies
type: note
---

## Investigation and link expansion — [[Decision making fallacies]] — 2026-09-24

> Lexical search only (1MCP tools were unavailable). I checked that every link target exists.

### What the note is

A stub hub. It was created in February 2025 (`ID: decision`, tag `fallacy`) with two links, [[Sunk Cost Fallacy]] and [[Appeal to Novelty]]. **Git history shows it has held exactly those two links in every version since 2025-11-09**, so nothing was lost; it was started as a list and never filled in.

### Where it was meant to fit

- Both linked notes use the same "Definition / Software Context / Example" template, as does [[Knowledge-Related Biases]]. They came from [[Thinking Patterns, Biases, and Heuristics in Development]], whose section 5.2, "Common Cognitive Biases in Software Development", is **empty**.
- [[MOC - Cognitive Biases]] section 3, "Decision-Making Biases", listed Sunk Cost Fallacy and Confirmation Bias as unlinked "(Placeholder)" lines.

So the note is the decision-making counterpart to [[Knowledge-Related Biases]], intended to hold the software-cognition series' decision fallacies.

### Links added (20 new, grouped)

| Group | Notes |
|---|---|
| Commitment and cost | [[Commitment, Consistency, and Sunk Cost Fallacy]], [[Goal Displacement]] |
| Novelty and fixation | [[Novelty Effect]], [[Claim - Novelty-craving drives self-defeating system-hopping]], [[The Einstellung Effect Prevents Better Solutions]], [[Satisficing Leads to Sub-optimal Solutions]] |
| Weighing gains, losses and time | [[Loss Aversion Describes Asymmetric Pain of Loss vs Pleasure of Gain]], [[Prospect Theory Models Decision-Making Relative to a Reference Point]], [[The Emotional Cost of Being Wrong is Magnified by Loss Aversion]], [[Temporal Discounting is the Cognitive Bias Where People Value Immediate Rewards More]], [[Action Dominance is the Cognitive Bias Towards Action Over Inaction]] |
| Judging evidence and outcomes | [[Confirmation as a Perceived Shortcut to Truth]], [[Goals Suffer from Survivorship Bias]], [[Selective Citation of Successful Predictions Creates a Hindsight-Bias Illusion of Predictive Skill]] |
| Stalling instead of deciding | [[SoT - Perfectionism and Analysis Paralysis]], [[Executive Dysfunction - The Root of Analysis Paralysis]], [[Information-Seeking Is Adaptive Only While It Remains Instrumental to an Actual Decision]] |
| Countermeasures | [[Decoupling Ego from Outcomes to Improve Decisions]], [[SoT - Commitment Devices (Ulysses Pacts)]], [[Choice Architecture Designs the Environment to Make Desired Behaviors Easier]] |

Each link has a one-line annotation. The two original links are kept and annotated. Borderline inclusions: [[Goal Displacement]], [[Goals Suffer from Survivorship Bias]] and the countermeasures are decision-adjacent rather than pure fallacies; remove any you disagree with.

### Other changes

| File | Change |
|---|---|
| The note | `type` `permanent` → `map`, `conformant: true`, tags `decision-making`, `fallacy`, `type/moc`; short intro; a See Also section |
| MOC - Cognitive Biases | the Sunk Cost placeholder is now a real link, with a pointer to this hub |
| Thinking Patterns, Biases, and Heuristics in Development | a "See" line under the empty section 5.2 |

### Left alone

- **Confirmation Bias** is still an unlinked placeholder in the MoC: no note by that name exists, and [[Confirmation as a Perceived Shortcut to Truth]] is a related but different note, so I did not stand it in.
- **The parent note** embeds two notes that do not exist (`Problem-Solving Strategies and Heuristics of Expert Developers`) and links to `Unravelling the Cognitive Landscape of Software Development`, which also does not exist. Not fixed.
- **Missing candidates:** no notes exist for anchoring, the planning fallacy, escalation of commitment or the endowment effect. They would be natural additions to this hub if you write them.
- The note lives in `100_zettelkasten` although it works as a MoC, so it sits outside the usual `MoC/` folder.

### Validation

Whole-vault `edge_lint.py`: `0 error(s), 0 warning(s)` (2886 notes, 1389 edges).
