---
conformant: true
created: 2026-09-14T00:00:00+00:00
modified: 2026-09-26T08:46:10+00:00
permalink: llmeon/30-library/so-t/protocol-diagnose-an-agent-failure
related: ["[[00 - Prompt Library Router]]", "[[prodos-agent-architecture-upgrade]]", "[[Protocol - Typed Answer Contract (TAC) for Vault Agents]]", "[[SoT - Agentic AI Design Patterns]]"]
tags: [domain/pkm, prodos/protocol, topic/agent-architecture, topic/evaluation]
title: Protocol - Diagnose an Agent Failure
type: protocol
---

> Promoted 2026-09-14 from a draft persona prompt captured in `00_Inbox/how does this fit with my prodOS@LLMeon protocol?.md` (see [[prodos-agent-architecture-upgrade]]) into a real, linkable Protocol note. Use this whenever an agent's output was wrong, unsafe, incomplete, non-conformant, or otherwise unsatisfactory—before editing a prompt, a note, or a script in response to it.

## Trigger

A human correction, an agent self-catch, or a review surfaces a result that shouldn't have happened. Run this protocol before making any corrective change.

## Steps

1. Preserve the original task, retrieved context, agent output, expected outcome, and observed failure. Don't patch first and reconstruct the failure from memory later—write down what actually happened while it's still available.
2. Classify the root cause. Pick exactly one (the closest fit, not several):
   - `retrieval-failure`—the right note existed but wasn't found/read.
   - `missing-or-stale-knowledge`—no note held the needed information, or it was outdated.
   - `taxonomy-or-routing-failure`—the agent misjudged what kind of note/content it was looking at (its folder, type, or authority level), or picked the wrong routing path. See [[10_System/evals/behavioral/behav-001-inbox-not-authoritative]] for a worked example.
   - `ambiguous-terminology`—a term meant two different things and the agent picked the wrong one without noticing.
   - `reasoning-recipe-failure`—the right recipe existed but was applied incorrectly, or the wrong recipe was chosen.
   - `tac-or-output-validation-failure`—the output didn't conform to the required Typed Answer Contract or note schema.
   - `permission-or-gateway-failure`—the agent acted (or refused to act) when the authorization rules said otherwise. See [[10_System/evals/behavioral/behav-002-dont-resolve-permission-conflicts-alone]] for the pattern to protect (escalate, don't self-resolve).
   - `tool-failure`—a tool/script itself misbehaved (crashed, returned wrong data), independent of the agent's reasoning.
   - `genuine-unresolved-ambiguity`—there wasn't enough information for anyone (human or agent) to have done better at the time.
   - `unclear-user-requirement`—the task itself was underspecified; the agent guessed instead of asking.
3. Propose the smallest corrective change at the responsible layer. A retrieval failure gets fixed by improving retrieval (a routing index, a clearer note title)—not by stuffing more instructions into an unrelated prompt. A reasoning-recipe failure gets fixed by editing that recipe, not by adding a special case elsewhere.
4. Avoid compensating for a retrieval failure by stuffing unrelated text into prompts. If the fix doesn't match the root-cause layer, it's very likely papering over the symptom rather than the cause.
5. Define a regression case that would fail before the change and pass after it. If the failure is structural (something `edge_lint.py` or `validate_note_frontmatter.py` could mechanically check), add it to `10_System/evals/structural/` and verify it fails against the old behaviour before your fix, then passes after. If it's a judgment call, add it to `10_System/evals/behavioral/` as a documented case—see `10_System/evals/README.md` for the format and the honest limits of what's actually machine-checked today.
6. Return the proposed correction and regression case together for review, not the correction alone. A fix without a regression case is a one-off patch, not a lasting improvement—see [[SoT - Agentic AI Design Patterns]] §2E ("Learning & Adaptation").

## Verification

The protocol was followed correctly if: the root cause has exactly one classification (not a vague "something went wrong"), the fix touches only the responsible layer, and a regression case exists that would have caught the original failure.

## Related

- [[The Illusion of Shared Understanding in Teams]]—_The mechanism behind the `ambiguous-terminology` and `unclear-user-requirement` classes: shared words hide differing models, so the mismatch surfaces only when the output is wrong._
